"""
Cliente para persistencia de contactos.

Este módulo maneja la persistencia de contactos en PostgreSQL
usando SQLAlchemy ORM, con soporte legacy para API REST externa.
"""

from typing import Dict, Any, Optional
from datetime import datetime
from uuid import uuid4

from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError

import httpx

from ..models.contact import Contact
from ..utils.logger import get_logger

logger = get_logger(__name__)

# Base para modelos SQLAlchemy
Base = declarative_base()


class ContactDB(Base):
    """
    Modelo de base de datos para contactos.

    Tabla: contacts
    """
    __tablename__ = "contacts"

    id = Column(String(36), primary_key=True)
    nombre = Column(String(255), nullable=False)
    telefono = Column(String(20), nullable=False)
    quien_lo_recomendo = Column(String(255), nullable=False)
    timestamp = Column(DateTime, nullable=False)
    source = Column(String(50), default="telegram")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ContactsAPIClient:
    """
    Cliente para persistencia de contactos en PostgreSQL.

    Attributes:
        database_url: URL de conexión a PostgreSQL.
        engine: Motor de SQLAlchemy.
        SessionLocal: Factory de sesiones.
        legacy_api_url: URL de API REST externa (opcional).
        legacy_api_key: API key para API externa (opcional).
    """

    def __init__(
        self,
        database_url: str,
        legacy_api_url: Optional[str] = None,
        legacy_api_key: Optional[str] = None,
        timeout: int = 10
    ):
        """
        Inicializa el cliente de contactos.

        Args:
            database_url: URL de conexión a PostgreSQL.
            legacy_api_url: URL de API REST externa (opcional).
            legacy_api_key: API key para API externa (opcional).
            timeout: Timeout para requests HTTP (default: 10).

        Example:
            >>> client = ContactsAPIClient(
            ...     database_url="postgresql://user:pass@localhost/db"
            ... )
        """
        self.database_url = database_url
        self.legacy_api_url = legacy_api_url
        self.legacy_api_key = legacy_api_key
        self.timeout = timeout

        # Configurar SQLAlchemy
        self.engine = create_engine(database_url, echo=False)
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

        logger.info(
            "contacts_api_client_initialized",
            database_url=database_url.split("@")[-1],  # Ocultar credenciales
            has_legacy_api=bool(legacy_api_url)
        )

    def create_tables(self) -> None:
        """
        Crea las tablas en la base de datos si no existen.

        Example:
            >>> client = ContactsAPIClient(database_url="...")
            >>> client.create_tables()
        """
        try:
            Base.metadata.create_all(bind=self.engine)
            logger.info("database_tables_created")
        except SQLAlchemyError as e:
            logger.error("failed_to_create_tables", error=str(e))
            raise

    async def save_contact(self, contact: Contact) -> Dict[str, Any]:
        """
        Guarda un contacto en PostgreSQL.

        Args:
            contact: Instancia del modelo Contact.

        Returns:
            dict con keys:
                - success: bool
                - contact_id: str (UUID del contacto si success=True)
                - error: str (mensaje de error si success=False)

        Example:
            >>> client = ContactsAPIClient(database_url="...")
            >>> contact = Contact(
            ...     nombre="Juan", telefono="+573001234567",
            ...     quien_lo_recomendo="María"
            ... )
            >>> result = await client.save_contact(contact)
            >>> result["success"]
            True
        """
        logger.info(
            "saving_contact",
            nombre=contact.nombre,
            telefono=contact.telefono
        )

        db: Session = self.SessionLocal()

        try:
            # Crear registro en base de datos
            contact_db = ContactDB(
                id=contact.id,
                nombre=contact.nombre,
                telefono=contact.telefono,
                quien_lo_recomendo=contact.quien_lo_recomendo,
                timestamp=contact.timestamp,
                source=contact.source
            )

            db.add(contact_db)
            db.commit()
            db.refresh(contact_db)

            logger.info(
                "contact_saved_successfully",
                contact_id=contact_db.id,
                nombre=contact_db.nombre
            )

            # Si hay API legacy configurada, también enviar allá
            if self.legacy_api_url:
                await self._save_to_legacy_api(contact)

            return {
                "success": True,
                "contact_id": contact_db.id
            }

        except SQLAlchemyError as e:
            db.rollback()
            logger.error(
                "failed_to_save_contact",
                error=str(e),
                error_type=type(e).__name__
            )
            return {
                "success": False,
                "error": f"Error al guardar contacto: {str(e)}"
            }

        finally:
            db.close()

    async def _save_to_legacy_api(self, contact: Contact) -> None:
        """
        Guarda el contacto en la API REST externa (legacy).

        Args:
            contact: Instancia del modelo Contact.
        """
        if not self.legacy_api_url or not self.legacy_api_key:
            return

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.legacy_api_url}/contacts",
                    json={
                        "nombre": contact.nombre,
                        "telefono": contact.telefono,
                        "quien_lo_recomendo": contact.quien_lo_recomendo,
                        "timestamp": contact.timestamp.isoformat(),
                        "source": contact.source
                    },
                    headers={
                        "Authorization": f"Bearer {self.legacy_api_key}",
                        "Content-Type": "application/json"
                    }
                )

                response.raise_for_status()

                logger.info(
                    "contact_saved_to_legacy_api",
                    status_code=response.status_code
                )

        except httpx.HTTPStatusError as e:
            logger.warning(
                "legacy_api_http_error",
                status_code=e.response.status_code,
                error=str(e)
            )

        except httpx.TimeoutException:
            logger.warning(
                "legacy_api_timeout",
                timeout=self.timeout
            )

        except Exception as e:
            logger.warning(
                "legacy_api_error",
                error=str(e)
            )

    async def get_contact(self, contact_id: str) -> Optional[Contact]:
        """
        Obtiene un contacto por su ID.

        Args:
            contact_id: UUID del contacto.

        Returns:
            Instancia de Contact o None si no existe.
        """
        db: Session = self.SessionLocal()

        try:
            contact_db = db.query(ContactDB).filter(
                ContactDB.id == contact_id
            ).first()

            if not contact_db:
                logger.warning("contact_not_found", contact_id=contact_id)
                return None

            # Convertir a modelo Pydantic
            contact = Contact(
                id=contact_db.id,
                nombre=contact_db.nombre,
                telefono=contact_db.telefono,
                quien_lo_recomendo=contact_db.quien_lo_recomendo,
                timestamp=contact_db.timestamp,
                source=contact_db.source,
                created_at=contact_db.created_at,
                updated_at=contact_db.updated_at
            )

            return contact

        except SQLAlchemyError as e:
            logger.error("failed_to_get_contact", error=str(e))
            return None

        finally:
            db.close()

    async def health_check(self) -> bool:
        """
        Verifica la conexión a la base de datos.

        Returns:
            True si la conexión es exitosa, False en caso contrario.
        """
        try:
            db: Session = self.SessionLocal()
            # Ejecutar query simple
            db.execute("SELECT 1")
            db.close()

            logger.info("database_health_check_passed")
            return True

        except Exception as e:
            logger.error(
                "database_health_check_failed",
                error=str(e)
            )
            return False

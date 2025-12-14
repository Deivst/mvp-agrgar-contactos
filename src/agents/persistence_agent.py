"""
Agente de Persistencia.

Este módulo implementa el agente encargado de:
- Guardar contactos en PostgreSQL
- Enviar confirmaciones al usuario
- Generar y enviar vCard
- Crear botón inline de Telegram
"""

from typing import Dict, Any

from ..models.contact import Contact
from ..services.contacts_api import ContactsAPIClient
from ..services.telegram_service import TelegramService
from ..utils.logger import get_logger
from ..utils.helpers import format_contact_message

logger = get_logger(__name__)


class PersistenceAgent:
    """
    Agente de persistencia para guardar contactos.

    Este agente coordina:
    1. Guardado en PostgreSQL
    2. Notificación al usuario con mensaje de confirmación
    3. Envío de archivo vCard para agregar a contactos
    4. Envío de botón inline de Telegram

    Attributes:
        contacts_client: Cliente de la API de contactos (PostgreSQL).
        telegram_service: Servicio de Telegram.
    """

    def __init__(
        self,
        contacts_client: ContactsAPIClient,
        telegram_service: TelegramService
    ):
        """
        Inicializa el agente de persistencia.

        Args:
            contacts_client: Instancia de ContactsAPIClient.
            telegram_service: Instancia de TelegramService.

        Example:
            >>> contacts_client = ContactsAPIClient(database_url="...")
            >>> telegram_service = TelegramService(bot_token="...")
            >>> agent = PersistenceAgent(contacts_client, telegram_service)
        """
        self.contacts_client = contacts_client
        self.telegram_service = telegram_service

        logger.info("persistence_agent_initialized")

    async def save_and_notify(
        self,
        contact_data: Dict[str, Any],
        chat_id: int
    ) -> Dict[str, Any]:
        """
        Guarda un contacto y notifica al usuario con vCard y botón.

        Este es el método principal que implementa la funcionalidad CRÍTICA
        del sistema:
        1. Guarda el contacto en PostgreSQL
        2. Envía confirmación al usuario
        3. Envía archivo vCard (.vcf) para descarga
        4. Envía botón inline de Telegram para agregar contacto

        Args:
            contact_data: Diccionario con datos del contacto
                (nombre, telefono, quien_lo_recomendo).
            chat_id: ID del chat de Telegram para notificaciones.

        Returns:
            dict con keys:
                - success: bool
                - contact_id: str (si success=True)
                - error: str (si success=False)

        Example:
            >>> agent = PersistenceAgent(contacts_client, telegram_service)
            >>> result = await agent.save_and_notify(
            ...     contact_data={
            ...         "nombre": "Juan Pérez",
            ...         "telefono": "+573001234567",
            ...         "quien_lo_recomendo": "María"
            ...     },
            ...     chat_id=123456
            ... )
            >>> result["success"]
            True
        """
        logger.info(
            "saving_and_notifying",
            nombre=contact_data.get("nombre"),
            chat_id=chat_id
        )

        try:
            # 1. Crear modelo Contact con validación Pydantic
            # Esto valida y normaliza:
            # - Teléfono: formato +57XXXXXXXXXX (10-15 dígitos)
            # - Nombres: sin espacios extras
            # - Longitudes correctas
            contact = Contact(
                nombre=contact_data["nombre"],
                telefono=contact_data["telefono"],
                quien_lo_recomendo=contact_data["quien_lo_recomendo"],
                source="telegram"
            )

            # 2. Guardar en PostgreSQL
            save_result = await self.contacts_client.save_contact(contact)

            if not save_result["success"]:
                logger.error(
                    "failed_to_save_contact",
                    error=save_result.get("error")
                )

                # Notificar error al usuario
                await self.telegram_service.send_error_message(
                    chat_id=chat_id,
                    error="No se pudo guardar el contacto",
                    details=save_result.get("error")
                )

                return save_result

            contact_id = save_result["contact_id"]

            logger.info(
                "contact_saved_successfully",
                contact_id=contact_id,
                nombre=contact.nombre
            )

            # 3. Preparar mensaje de confirmación
            confirmation_message = format_contact_message(
                nombre=contact.nombre,
                telefono=contact.telefono,
                quien_lo_recomendo=contact.quien_lo_recomendo,
                contact_id=contact_id
            )

            # 4. Enviar confirmación + vCard + botón de Telegram
            # Esta es la funcionalidad CRÍTICA del sistema
            notification_sent = await self.telegram_service.send_contact_with_vcard_and_button(
                chat_id=chat_id,
                nombre=contact.nombre,
                telefono=contact.telefono,
                quien_lo_recomendo=contact.quien_lo_recomendo,
                confirmation_message=confirmation_message
            )

            if not notification_sent:
                logger.warning(
                    "notification_failed",
                    contact_id=contact_id,
                    chat_id=chat_id
                )
                # El contacto ya está guardado, pero la notificación falló
                # No es un error crítico

            logger.info(
                "contact_saved_and_notified",
                contact_id=contact_id,
                chat_id=chat_id,
                notification_sent=notification_sent
            )

            return {
                "success": True,
                "contact_id": contact_id
            }

        except ValueError as e:
            # Error de validación de Pydantic (teléfono, nombre, etc.)
            logger.warning(
                "pydantic_validation_error",
                error=str(e),
                nombre=contact_data.get("nombre")
            )

            # Notificar error de validación al usuario
            await self.telegram_service.send_error_message(
                chat_id=chat_id,
                error="Datos inválidos",
                details=str(e)
            )

            return {
                "success": False,
                "error": f"Validación fallida: {str(e)}",
                "error_type": "validation_error"
            }

        except Exception as e:
            logger.error(
                "persistence_agent_error",
                error=str(e),
                error_type=type(e).__name__
            )

            # Notificar error al usuario
            await self.telegram_service.send_error_message(
                chat_id=chat_id,
                error="Error inesperado al guardar el contacto",
                details=str(e)
            )

            return {
                "success": False,
                "error": f"Error inesperado: {str(e)}"
            }

    async def save_contact(self, contact: Contact) -> Dict[str, Any]:
        """
        Guarda un contacto sin enviar notificaciones.

        Args:
            contact: Instancia del modelo Contact.

        Returns:
            dict con success y contact_id o error.
        """
        return await self.contacts_client.save_contact(contact)

    async def health_check(self) -> bool:
        """
        Verifica el estado de los servicios del agente.

        Returns:
            True si todos los servicios están operativos, False en caso contrario.
        """
        db_health = await self.contacts_client.health_check()
        telegram_health = await self.telegram_service.health_check()

        is_healthy = db_health and telegram_health

        logger.info(
            "persistence_agent_health_check",
            db_health=db_health,
            telegram_health=telegram_health,
            is_healthy=is_healthy
        )

        return is_healthy

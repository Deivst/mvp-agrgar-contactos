"""
Modelo de datos para contactos.

Este módulo define el modelo Contact que representa un contacto
en el sistema de gestión de contactos.
"""

from datetime import datetime
from typing import Literal, Optional
import re
from uuid import uuid4

from pydantic import BaseModel, Field, field_validator


class Contact(BaseModel):
    """
    Modelo de datos para un contacto.

    Attributes:
        id: Identificador único del contacto (UUID).
        nombre: Nombre completo del contacto.
        telefono: Número de teléfono normalizado (formato +57XXXXXXXXXX).
        quien_lo_recomendo: Nombre de la persona que recomendó el contacto.
        timestamp: Fecha y hora de registro del contacto.
        source: Origen del contacto (telegram, api, manual).
        created_at: Fecha de creación en base de datos.
        updated_at: Fecha de última actualización.

    Example:
        >>> contact = Contact(
        ...     nombre="Juan Pérez",
        ...     telefono="300 123 4567",
        ...     quien_lo_recomendo="María López"
        ... )
        >>> print(contact.telefono)
        +573001234567
    """

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Identificador único UUID"
    )

    nombre: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Nombre completo del contacto"
    )

    telefono: str = Field(
        ...,
        description="Número de teléfono (se normaliza automáticamente)"
    )

    quien_lo_recomendo: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Nombre de quien recomendó el contacto"
    )

    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Fecha y hora de registro"
    )

    source: Literal["telegram", "api", "manual"] = Field(
        default="telegram",
        description="Origen del contacto"
    )

    created_at: Optional[datetime] = Field(
        default=None,
        description="Fecha de creación en BD"
    )

    updated_at: Optional[datetime] = Field(
        default=None,
        description="Fecha de actualización en BD"
    )

    @field_validator("telefono")
    @classmethod
    def validate_and_normalize_phone(cls, value: str) -> str:
        """
        Valida y normaliza el número de teléfono.

        Args:
            value: Número de teléfono en cualquier formato.

        Returns:
            Número normalizado en formato +57XXXXXXXXXX.

        Raises:
            ValueError: Si el número no tiene entre 10 y 15 dígitos.
        """
        if not value:
            raise ValueError("El teléfono no puede estar vacío")

        # Remover todo excepto dígitos y +
        cleaned = re.sub(r"[^\d+]", "", value)

        # Extraer solo dígitos para validar longitud
        digits_only = cleaned.replace("+", "")

        if len(digits_only) < 10:
            raise ValueError(
                f"El teléfono debe tener al menos 10 dígitos, "
                f"se encontraron {len(digits_only)}"
            )

        if len(digits_only) > 15:
            raise ValueError(
                f"El teléfono no puede tener más de 15 dígitos, "
                f"se encontraron {len(digits_only)}"
            )

        # Agregar código de país si no existe
        if not cleaned.startswith("+"):
            # Asumir código de país +57 (Colombia)
            cleaned = "+57" + cleaned

        return cleaned

    @field_validator("nombre", "quien_lo_recomendo")
    @classmethod
    def validate_and_clean_names(cls, value: str) -> str:
        """
        Valida y limpia campos de nombre.

        Args:
            value: Nombre a validar.

        Returns:
            Nombre limpio sin espacios extras.

        Raises:
            ValueError: Si el nombre está vacío después de limpiar.
        """
        if not value:
            raise ValueError("El campo no puede estar vacío")

        # Remover espacios extras (inicio, fin, y múltiples espacios internos)
        cleaned = " ".join(value.split())

        if not cleaned:
            raise ValueError("El campo no puede contener solo espacios")

        return cleaned

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "nombre": "Juan Carlos Pérez García",
                "telefono": "+573001234567",
                "quien_lo_recomendo": "María López Rodríguez",
                "timestamp": "2025-01-15T10:30:00Z",
                "source": "telegram",
                "created_at": "2025-01-15T10:30:00Z",
                "updated_at": "2025-01-15T10:30:00Z"
            }
        }
    }

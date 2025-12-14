"""
Validador de mensajes de Telegram.

Este módulo valida el formato y contenido de los mensajes
antes de procesarlos.
"""

from typing import Dict, Any, Optional
from ..utils.logger import get_logger

logger = get_logger(__name__)


class MessageValidator:
    """
    Validador de mensajes de Telegram.

    Attributes:
        min_length: Longitud mínima del mensaje.
        max_length: Longitud máxima del mensaje.
    """

    def __init__(self, min_length: int = 5, max_length: int = 1000):
        """
        Inicializa el validador de mensajes.

        Args:
            min_length: Longitud mínima permitida (default: 5).
            max_length: Longitud máxima permitida (default: 1000).
        """
        self.min_length = min_length
        self.max_length = max_length

    def validate(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida un mensaje de Telegram.

        Args:
            message: Diccionario con datos del mensaje.
                Expected keys: text, user_id, chat_id

        Returns:
            dict con keys:
                - valid: bool
                - error: str (si valid=False)
                - message: dict (mensaje original si valid=True)

        Example:
            >>> validator = MessageValidator()
            >>> result = validator.validate({
            ...     "text": "Juan 3001234567 ref María",
            ...     "user_id": 123,
            ...     "chat_id": 456
            ... })
            >>> result["valid"]
            True
        """
        # Validar que existan los campos requeridos
        required_fields = ["text", "user_id", "chat_id"]
        for field in required_fields:
            if field not in message:
                logger.warning(
                    "missing_required_field",
                    field=field,
                    message_keys=list(message.keys())
                )
                return {
                    "valid": False,
                    "error": f"Campo requerido faltante: {field}"
                }

        text = message.get("text", "")

        # Validar que el texto no esté vacío
        if not text or not text.strip():
            logger.warning(
                "empty_message",
                user_id=message.get("user_id")
            )
            return {
                "valid": False,
                "error": "El mensaje no puede estar vacío"
            }

        # Validar longitud mínima
        if len(text.strip()) < self.min_length:
            logger.warning(
                "message_too_short",
                user_id=message.get("user_id"),
                length=len(text.strip()),
                min_length=self.min_length
            )
            return {
                "valid": False,
                "error": f"El mensaje es muy corto. Mínimo {self.min_length} caracteres."
            }

        # Validar longitud máxima
        if len(text) > self.max_length:
            logger.warning(
                "message_too_long",
                user_id=message.get("user_id"),
                length=len(text),
                max_length=self.max_length
            )
            return {
                "valid": False,
                "error": f"El mensaje es muy largo. Máximo {self.max_length} caracteres."
            }

        logger.debug(
            "message_validation_passed",
            user_id=message.get("user_id"),
            text_length=len(text)
        )

        return {
            "valid": True,
            "message": message
        }

    def validate_text_only(self, text: str) -> bool:
        """
        Valida solo el texto del mensaje.

        Args:
            text: Texto a validar.

        Returns:
            True si el texto es válido, False en caso contrario.
        """
        if not text or not text.strip():
            return False

        if len(text.strip()) < self.min_length:
            return False

        if len(text) > self.max_length:
            return False

        return True

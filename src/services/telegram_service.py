"""
Servicio de integración con Telegram Bot API.

Este módulo maneja la comunicación con Telegram, incluyendo
envío de mensajes, vCards y botones inline.
"""

from typing import Optional
from io import BytesIO

from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from ..utils.logger import get_logger
from ..utils.helpers import (
    generate_vcard,
    vcard_to_bytes,
    normalize_phone_for_telegram
)

logger = get_logger(__name__)


class TelegramService:
    """
    Servicio para interacción con Telegram Bot API.

    Attributes:
        bot_token: Token del bot de Telegram.
        bot: Instancia del bot de Telegram.
    """

    def __init__(self, bot_token: str):
        """
        Inicializa el servicio de Telegram.

        Args:
            bot_token: Token del bot de Telegram.

        Example:
            >>> service = TelegramService(bot_token="your-bot-token")
        """
        self.bot_token = bot_token
        self.bot = Bot(token=bot_token)

        logger.info("telegram_service_initialized")

    async def send_message(
        self,
        chat_id: int,
        text: str,
        parse_mode: Optional[str] = None
    ) -> bool:
        """
        Envía un mensaje de texto a un chat.

        Args:
            chat_id: ID del chat de destino.
            text: Texto del mensaje.
            parse_mode: Modo de parseo (HTML, Markdown, etc).

        Returns:
            True si el mensaje se envió correctamente, False en caso contrario.

        Example:
            >>> service = TelegramService(bot_token="token")
            >>> await service.send_message(123, "Hola mundo")
            True
        """
        try:
            await self.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode=parse_mode
            )

            logger.info(
                "message_sent",
                chat_id=chat_id,
                text_length=len(text)
            )

            return True

        except Exception as e:
            logger.error(
                "failed_to_send_message",
                chat_id=chat_id,
                error=str(e)
            )
            return False

    async def send_contact_with_vcard_and_button(
        self,
        chat_id: int,
        nombre: str,
        telefono: str,
        quien_lo_recomendo: str,
        confirmation_message: str
    ) -> bool:
        """
        Envía un vCard para agregar automáticamente el contacto a la libreta.

        Esta es la forma más automática: al abrir el vCard en el teléfono,
        automáticamente pregunta si desea agregarlo a contactos.

        Args:
            chat_id: ID del chat de destino.
            nombre: Nombre del contacto.
            telefono: Teléfono del contacto (formato +57...).
            quien_lo_recomendo: Nombre del referido.
            confirmation_message: Mensaje de confirmación a mostrar.

        Returns:
            True si se envió correctamente, False en caso contrario.

        Example:
            >>> service = TelegramService(bot_token="token")
            >>> await service.send_contact_with_vcard_and_button(
            ...     chat_id=123,
            ...     nombre="Juan Pérez",
            ...     telefono="+573001234567",
            ...     quien_lo_recomendo="María",
            ...     confirmation_message="Contacto guardado"
            ... )
            True
        """
        try:
            # Generar vCard
            vcard_content = generate_vcard(nombre, telefono, quien_lo_recomendo)
            vcard_bytes = vcard_to_bytes(vcard_content)

            # Enviar el vCard como documento con nombre .vcf
            # Cuando el usuario lo toca, automáticamente abre la opción de agregar a contactos
            await self.bot.send_document(
                chat_id=chat_id,
                document=vcard_bytes,
                filename=f"{nombre.replace(' ', '_')}.vcf",
                caption=f"📇 {nombre}\n☝️ Toca para agregar automáticamente a tus contactos"
            )

            logger.info(
                "vcard_sent_for_auto_save",
                chat_id=chat_id,
                nombre=nombre
            )

            return True

        except Exception as e:
            logger.error(
                "failed_to_send_vcard",
                chat_id=chat_id,
                error=str(e)
            )
            return False

    async def send_error_message(
        self,
        chat_id: int,
        error: str,
        details: Optional[str] = None
    ) -> bool:
        """
        Envía un mensaje de error formateado al usuario.

        Args:
            chat_id: ID del chat de destino.
            error: Mensaje de error principal.
            details: Detalles adicionales del error (opcional).

        Returns:
            True si se envió correctamente, False en caso contrario.
        """
        from ..utils.helpers import format_error_message

        message = format_error_message(error, details)
        return await self.send_message(chat_id, message)

    async def get_bot_info(self) -> dict:
        """
        Obtiene información del bot.

        Returns:
            Diccionario con información del bot.
        """
        try:
            me = await self.bot.get_me()
            return {
                "id": me.id,
                "username": me.username,
                "first_name": me.first_name,
                "is_bot": me.is_bot
            }

        except Exception as e:
            logger.error("failed_to_get_bot_info", error=str(e))
            return {}

    async def health_check(self) -> bool:
        """
        Verifica que el bot esté funcionando.

        Returns:
            True si el bot está disponible, False en caso contrario.
        """
        try:
            await self.bot.get_me()
            logger.info("telegram_health_check_passed")
            return True

        except Exception as e:
            logger.error(
                "telegram_health_check_failed",
                error=str(e)
            )
            return False

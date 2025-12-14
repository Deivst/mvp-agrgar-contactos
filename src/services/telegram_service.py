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
        Envía un contacto guardado con vCard y botón de Telegram.

        Esta es la funcionalidad CRÍTICA del sistema que permite al usuario
        agregar el contacto a su libreta de dos formas:
        1. Descargando el archivo vCard (.vcf)
        2. Usando el botón inline de Telegram

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
            # 1. Enviar mensaje de confirmación
            await self.send_message(chat_id, confirmation_message)

            # 2. Generar y enviar archivo vCard
            vcard_content = generate_vcard(nombre, telefono, quien_lo_recomendo)
            vcard_bytes = vcard_to_bytes(vcard_content)
            vcard_bytes.name = f"{nombre.replace(' ', '_')}.vcf"

            await self.bot.send_document(
                chat_id=chat_id,
                document=vcard_bytes,
                filename=f"{nombre.replace(' ', '_')}.vcf",
                caption="📇 Archivo vCard - Toca para agregar a tus contactos"
            )

            logger.info(
                "vcard_sent",
                chat_id=chat_id,
                nombre=nombre
            )

            # 3. Enviar contacto usando la API NATIVA de Telegram (send_contact)
            # Esto es la forma MÁS automática posible - aparece directamente
            # como contacto que el usuario puede guardar con un toque

            # Separar nombre en first_name y last_name
            nombre_parts = nombre.strip().split(maxsplit=1)
            first_name = nombre_parts[0] if len(nombre_parts) > 0 else nombre
            last_name = nombre_parts[1] if len(nombre_parts) > 1 else ""

            # Normalizar teléfono para Telegram (quitar el +)
            phone_for_telegram = telefono.replace("+", "")

            # Enviar contacto nativo de Telegram
            await self.bot.send_contact(
                chat_id=chat_id,
                phone_number=phone_for_telegram,
                first_name=first_name,
                last_name=last_name,
                vcard=None  # Ya enviamos el vCard antes
            )

            # Enviar mensaje explicativo
            await self.bot.send_message(
                chat_id=chat_id,
                text="☝️ Toca el contacto de arriba y luego 'Agregar a Contactos' para guardarlo automáticamente"
            )

            logger.info(
                "contact_button_sent",
                chat_id=chat_id,
                nombre=nombre
            )

            return True

        except Exception as e:
            logger.error(
                "failed_to_send_contact_with_vcard",
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

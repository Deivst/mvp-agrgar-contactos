"""
Sistema Multi-Agente de Gestión de Contactos.

Punto de entrada principal del sistema. Orquesta todos los componentes
y maneja el bot de Telegram.
"""

import asyncio
from typing import Optional

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)

from config.settings import settings
from src.services.gemini_service import GeminiService
from src.services.contacts_api import ContactsAPIClient
from src.services.telegram_service import TelegramService
from src.agents.security_agent import SecurityAgent
from src.agents.persistence_agent import PersistenceAgent
from src.utils.logger import configure_logging, get_logger

# Configurar logging
configure_logging(log_level=settings.LOG_LEVEL, log_format=settings.LOG_FORMAT)
logger = get_logger(__name__)


class ContactsOrchestrator:
    """
    Orquestrador principal del sistema.

    Coordina todos los agentes y servicios para procesar
    mensajes de Telegram y gestionar contactos.

    Attributes:
        gemini_service: Servicio de Google Gemini.
        contacts_client: Cliente de PostgreSQL.
        telegram_service: Servicio de Telegram.
        security_agent: Agente de seguridad.
        persistence_agent: Agente de persistencia.
        application: Aplicación de python-telegram-bot.
    """

    def __init__(self):
        """Inicializa el orquestrador y todos los componentes."""
        logger.info(
            "initializing_contacts_orchestrator",
            environment=settings.ENVIRONMENT
        )

        # Inicializar servicios
        self.gemini_service = GeminiService(
            api_key=settings.GEMINI_API_KEY,
            model_name=settings.GEMINI_MODEL,
            timeout=settings.GEMINI_TIMEOUT
        )

        self.contacts_client = ContactsAPIClient(
            database_url=settings.DATABASE_URL,
            legacy_api_url=settings.CONTACTS_API_URL if settings.CONTACTS_API_URL else None,
            legacy_api_key=settings.CONTACTS_API_KEY if settings.CONTACTS_API_KEY else None,
            timeout=settings.CONTACTS_API_TIMEOUT
        )

        # Crear tablas en PostgreSQL si no existen
        try:
            self.contacts_client.create_tables()
            logger.info("database_tables_ready")
        except Exception as e:
            logger.error("failed_to_create_tables", error=str(e))
            raise

        self.telegram_service = TelegramService(
            bot_token=settings.TELEGRAM_BOT_TOKEN
        )

        # Inicializar agentes
        self.security_agent = SecurityAgent(
            gemini_service=self.gemini_service,
            allowed_users=settings.get_allowed_users(),
            max_requests=settings.RATE_LIMIT_REQUESTS,
            window_seconds=settings.RATE_LIMIT_WINDOW
        )

        self.persistence_agent = PersistenceAgent(
            contacts_client=self.contacts_client,
            telegram_service=self.telegram_service
        )

        # Crear aplicación de Telegram
        self.application = Application.builder().token(
            settings.TELEGRAM_BOT_TOKEN
        ).build()

        # Registrar handlers
        self._register_handlers()

        logger.info(
            "contacts_orchestrator_initialized",
            allowed_users=len(settings.get_allowed_users())
        )

    def _register_handlers(self) -> None:
        """Registra los handlers del bot de Telegram."""
        # Handler para comando /start
        self.application.add_handler(
            CommandHandler("start", self.start_command)
        )

        # Handler para comando /help
        self.application.add_handler(
            CommandHandler("help", self.help_command)
        )

        # Handler para comando /health
        self.application.add_handler(
            CommandHandler("health", self.health_command)
        )

        # Handler para callbacks de confirmación
        self.application.add_handler(
            CallbackQueryHandler(self.handle_confirmation, pattern="^(confirm|reject)_")
        )

        # Handler para mensajes de texto (procesamiento de contactos)
        self.application.add_handler(
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                self.handle_message
            )
        )

        logger.info("telegram_handlers_registered")

    async def start_command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handler para el comando /start.

        Args:
            update: Update de Telegram.
            context: Contexto de la conversación.
        """
        user = update.effective_user
        chat_id = update.effective_chat.id

        logger.info(
            "start_command_received",
            user_id=user.id,
            username=user.username
        )

        welcome_message = f"""👋 ¡Hola {user.first_name}!

Soy el bot de gestión de contactos.

📝 Para agregar un contacto, simplemente envíame un mensaje con:
- Nombre del contacto
- Número de teléfono
- Quién te lo recomendó

Ejemplo:
"Juan Pérez 3001234567 recomendado por María López"

🔒 Solo usuarios autorizados pueden usar este bot.

Usa /help para más información."""

        await context.bot.send_message(
            chat_id=chat_id,
            text=welcome_message
        )

    async def help_command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handler para el comando /help.

        Args:
            update: Update de Telegram.
            context: Contexto de la conversación.
        """
        chat_id = update.effective_chat.id

        help_message = """📚 Ayuda - Bot de Gestión de Contactos

🎯 Cómo agregar un contacto:
Envía un mensaje con la información del contacto. Por ejemplo:

"Juan Carlos Pérez
300 123 4567
Me lo recomendó María López"

O más informal:
"Juan 3001234567 ref María"

📋 Comandos disponibles:
/start - Mensaje de bienvenida
/help - Muestra esta ayuda
/health - Verifica el estado del sistema

✅ El sistema te enviará:
1. Confirmación del contacto guardado
2. Archivo vCard (.vcf) para descargar
3. Botón para agregar directamente a tus contactos

💡 Consejos:
- El formato puede ser flexible
- Incluye el código de país (+57) o se agregará automáticamente
- El sistema detecta automáticamente nombre, teléfono y referido"""

        await context.bot.send_message(
            chat_id=chat_id,
            text=help_message
        )

    async def health_command(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handler para el comando /health.

        Args:
            update: Update de Telegram.
            context: Contexto de la conversación.
        """
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id

        # Solo permitir a usuarios autorizados
        if user_id not in self.security_agent.allowed_users:
            await context.bot.send_message(
                chat_id=chat_id,
                text="❌ No tienes autorización para usar este comando."
            )
            return

        logger.info("health_check_requested", user_id=user_id)

        # Verificar salud de componentes
        gemini_health = await self.gemini_service.health_check()
        db_health = await self.contacts_client.health_check()
        telegram_health = await self.telegram_service.health_check()
        persistence_health = await self.persistence_agent.health_check()

        status_emoji = {
            True: "✅",
            False: "❌"
        }

        health_message = f"""🏥 Estado del Sistema

📡 Telegram Bot: {status_emoji[telegram_health]}
🤖 Google Gemini: {status_emoji[gemini_health]}
🗄️ PostgreSQL: {status_emoji[db_health]}
💾 Persistencia: {status_emoji[persistence_health]}

🌐 Entorno: {settings.ENVIRONMENT}
📊 Usuarios autorizados: {len(self.security_agent.allowed_users)}"""

        await context.bot.send_message(
            chat_id=chat_id,
            text=health_message
        )

    async def handle_message(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handler principal para mensajes de texto.

        Extrae la información del contacto y pide confirmación del usuario.

        Args:
            update: Update de Telegram.
            context: Contexto de la conversación.
        """
        user = update.effective_user
        chat_id = update.effective_chat.id
        message_text = update.message.text

        logger.info(
            "message_received",
            user_id=user.id,
            username=user.username,
            chat_id=chat_id,
            message_length=len(message_text)
        )

        # Preparar mensaje para el SecurityAgent
        message_data = {
            "text": message_text,
            "user_id": user.id,
            "chat_id": chat_id,
            "username": user.username
        }

        # Procesar con SecurityAgent (validación y extracción)
        security_result = await self.security_agent.process_request(message_data)

        if not security_result["success"]:
            # Enviar error al usuario
            error_type = security_result.get("error_type", "unknown")
            error_message = security_result["error"]

            logger.warning(
                "message_processing_failed",
                user_id=user.id,
                error_type=error_type,
                error=error_message
            )

            await self.telegram_service.send_error_message(
                chat_id=chat_id,
                error=error_message
            )
            return

        # Extraer datos del contacto
        contact_data = security_result["contact"]

        logger.info(
            "security_validation_passed",
            user_id=user.id,
            contact_nombre=contact_data["nombre"]
        )

        # Preparar mensaje de confirmación
        confirmation_message = self._format_contact_for_confirmation(contact_data)

        # Crear botones de confirmación
        keyboard = [
            [
                InlineKeyboardButton("✅ Sí, agregarlo", callback_data=f"confirm_{user.id}_{chat_id}"),
                InlineKeyboardButton("❌ No, cancelar", callback_data=f"reject_{user.id}_{chat_id}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Guardar la información del contacto en el contexto del usuario
        if not hasattr(context, "user_data"):
            context.user_data = {}
        
        context.user_data[f"pending_contact_{user.id}"] = {
            "contact": contact_data,
            "chat_id": chat_id,
            "user_id": user.id
        }

        # Enviar mensaje de confirmación
        await context.bot.send_message(
            chat_id=chat_id,
            text=confirmation_message,
            reply_markup=reply_markup
        )

    def _format_contact_for_confirmation(self, contact_data: dict) -> str:
        """
        Formatea los datos del contacto para mostrar al usuario.

        Args:
            contact_data: Diccionario con datos del contacto.

        Returns:
            Mensaje formateado.
        """
        nombre = contact_data.get("nombre", "N/A")
        telefono = contact_data.get("telefono", "N/A")
        referido = contact_data.get("quien_lo_recomendo", "N/A")

        message = f"""📋 Por favor confirma estos datos:

👤 Nombre: {nombre}
📞 Teléfono: {telefono}
👥 Recomendado por: {referido}

¿Estás de acuerdo en agregar este contacto a tu libreta?"""

        return message

    async def handle_confirmation(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handler para la confirmación o rechazo del contacto.

        Args:
            update: Update de Telegram.
            context: Contexto de la conversación.
        """
        query = update.callback_query
        user_id = query.from_user.id
        chat_id = query.message.chat_id
        
        # Obtener los datos del contacto pendiente
        pending_key = f"pending_contact_{user_id}"
        if pending_key not in context.user_data:
            await query.answer("❌ La sesión expiró. Por favor intenta de nuevo.", show_alert=True)
            return

        pending_contact = context.user_data[pending_key]
        contact_data = pending_contact["contact"]

        # Confirmar presión del botón
        await query.answer()

        if query.data.startswith("confirm_"):
            # Usuario confirmó - guardar contacto
            logger.info(
                "contact_confirmation_accepted",
                user_id=user_id,
                contact_nombre=contact_data["nombre"]
            )

            # Actualizar el mensaje a "Guardando..."
            await query.edit_message_text(
                text="⏳ Guardando contacto en tu libreta..."
            )

            # Guardar en la BD
            persistence_result = await self.persistence_agent.save_and_notify(
                contact_data=contact_data,
                chat_id=chat_id
            )

            if not persistence_result["success"]:
                logger.error(
                    "persistence_failed",
                    user_id=user_id,
                    error=persistence_result.get("error")
                )
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"❌ Error al guardar: {persistence_result.get('error')}"
                )
                return

            # Después de guardar exitosamente, actualizar mensaje
            await query.edit_message_text(
                text=f"✅ ¡Contacto guardado exitosamente!\n\n👤 {contact_data['nombre']}\n📞 {contact_data['telefono']}\n👥 Recomendado por: {contact_data['quien_lo_recomendo']}"
            )

        elif query.data.startswith("reject_"):
            # Usuario rechazó - cancelar
            logger.info(
                "contact_confirmation_rejected",
                user_id=user_id,
                contact_nombre=contact_data["nombre"]
            )

            await query.edit_message_text(
                text="❌ Contacto cancelado. No fue agregado a tu libreta."
            )

        # Limpiar datos del contacto pendiente
        if pending_key in context.user_data:
            del context.user_data[pending_key]

    async def run(self) -> None:
        """Inicia el bot de Telegram."""
        logger.info("starting_telegram_bot")

        # Obtener información del bot
        bot_info = await self.telegram_service.get_bot_info()
        logger.info(
            "bot_info",
            bot_id=bot_info.get("id"),
            bot_username=bot_info.get("username")
        )

        # Iniciar el bot
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling(drop_pending_updates=True)

        logger.info("telegram_bot_running")

        # Mantener el bot corriendo
        try:
            await asyncio.Event().wait()
        except (KeyboardInterrupt, SystemExit):
            logger.info("shutting_down_telegram_bot")
            await self.application.stop()


async def main() -> None:
    """Función principal."""
    logger.info(
        "starting_contacts_management_system",
        version="1.0.0",
        environment=settings.ENVIRONMENT
    )

    try:
        orchestrator = ContactsOrchestrator()
        await orchestrator.run()

    except Exception as e:
        logger.error(
            "fatal_error",
            error=str(e),
            error_type=type(e).__name__
        )
        raise


if __name__ == "__main__":
    asyncio.run(main())

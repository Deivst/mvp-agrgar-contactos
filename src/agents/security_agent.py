"""
Agente de Seguridad.

Este módulo implementa el agente principal de seguridad del sistema,
encargado de:
- Validación de usuarios autorizados
- Validación de formato de mensajes
- Sanitización de datos
- Rate limiting
- Procesamiento con Gemini
"""

from typing import Dict, Any, List, Set
from collections import defaultdict

from ..services.gemini_service import GeminiService
from ..validators.message_validator import MessageValidator
from ..validators.contact_validator import ContactValidator
from ..utils.logger import get_logger, SecurityLogger
from ..utils.rate_limiter import RateLimiter
from ..utils.helpers import DataSanitizer

logger = get_logger(__name__)
security_logger = SecurityLogger()


class SecurityAgent:
    """
    Agente de seguridad para validación y procesamiento de mensajes.

    Este agente coordina:
    1. Autenticación de usuarios (whitelist)
    2. Rate limiting
    3. Validación de mensajes
    4. Sanitización de datos
    5. Extracción de contactos con Gemini
    6. Validación de datos extraídos

    Attributes:
        allowed_users: Set de user IDs autorizados.
        blocked_users: Set de user IDs bloqueados.
        gemini_service: Servicio de extracción con Gemini.
        message_validator: Validador de mensajes.
        contact_validator: Validador de contactos.
        rate_limiter: Limitador de frecuencia de requests.
        failed_attempts: Contador de intentos fallidos por usuario.
    """

    def __init__(
        self,
        gemini_service: GeminiService,
        allowed_users: List[int],
        max_requests: int = 10,
        window_seconds: int = 60,
        max_failed_attempts: int = 5
    ):
        """
        Inicializa el agente de seguridad.

        Args:
            gemini_service: Instancia de GeminiService.
            allowed_users: Lista de user IDs autorizados.
            max_requests: Máximo de requests por ventana de tiempo.
            window_seconds: Duración de la ventana en segundos.
            max_failed_attempts: Intentos fallidos antes de bloquear.

        Example:
            >>> gemini = GeminiService(api_key="key")
            >>> agent = SecurityAgent(
            ...     gemini_service=gemini,
            ...     allowed_users=[123456789]
            ... )
        """
        self.allowed_users: Set[int] = set(allowed_users)
        self.blocked_users: Set[int] = set()
        self.gemini_service = gemini_service
        self.message_validator = MessageValidator()
        self.contact_validator = ContactValidator()
        self.rate_limiter = RateLimiter(
            max_requests=max_requests,
            window_seconds=window_seconds
        )
        self.failed_attempts: Dict[int, int] = defaultdict(int)
        self.max_failed_attempts = max_failed_attempts

        logger.info(
            "security_agent_initialized",
            allowed_users_count=len(self.allowed_users),
            max_requests=max_requests,
            window_seconds=window_seconds
        )

    async def process_request(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa una solicitud de mensaje de Telegram.

        Flujo de procesamiento:
        1. Validar origen (usuario autorizado)
        2. Verificar rate limit
        3. Validar formato del mensaje
        4. Sanitizar datos
        5. Extraer contacto con Gemini
        6. Validar datos extraídos

        Args:
            message: Diccionario con keys:
                - text: str - Contenido del mensaje
                - user_id: int - ID del usuario de Telegram
                - chat_id: int - ID del chat
                - username: str (opcional) - Username de Telegram

        Returns:
            dict: Resultado del procesamiento
                - success: bool
                - contact: dict (si success=True)
                - error: str (si success=False)
                - error_type: str (si success=False)

        Example:
            >>> agent = SecurityAgent(gemini_service, [123])
            >>> result = await agent.process_request({
            ...     "text": "Juan 3001234567 ref María",
            ...     "user_id": 123,
            ...     "chat_id": 456
            ... })
            >>> result["success"]
            True
        """
        user_id = message.get("user_id")
        username = message.get("username", "unknown")

        logger.info(
            "processing_request",
            user_id=user_id,
            username=username
        )

        # 1. Validar origen (autenticación)
        auth_result = self._validate_origin(user_id, username)
        if not auth_result["valid"]:
            return {
                "success": False,
                "error": auth_result["error"],
                "error_type": "unauthorized"
            }

        # 2. Verificar rate limit
        rate_limit_result = self._check_rate_limit(user_id, username)
        if not rate_limit_result["valid"]:
            return {
                "success": False,
                "error": rate_limit_result["error"],
                "error_type": "rate_limit_exceeded"
            }

        # 3. Validar formato del mensaje
        validation_result = self.message_validator.validate(message)
        if not validation_result["valid"]:
            self.failed_attempts[user_id] += 1
            return {
                "success": False,
                "error": validation_result["error"],
                "error_type": "invalid_message_format"
            }

        # 4. Sanitizar datos
        sanitized_text = DataSanitizer.sanitize(message["text"])

        if not DataSanitizer.is_safe(message["text"]):
            security_logger.log_suspicious_input(
                user_id=user_id,
                input_type="dangerous_pattern"
            )

            self.failed_attempts[user_id] += 1

            return {
                "success": False,
                "error": "El mensaje contiene patrones sospechosos",
                "error_type": "suspicious_input"
            }

        # 5. Extraer contacto con Gemini
        extraction_result = await self.gemini_service.extract_contact_info(
            sanitized_text
        )

        if not extraction_result["success"]:
            self.failed_attempts[user_id] += 1
            logger.warning(
                "gemini_extraction_failed",
                user_id=user_id,
                error=extraction_result.get("error")
            )

            return {
                "success": False,
                "error": "No pude procesar el mensaje. Por favor, incluye: nombre, teléfono y quién te lo recomendó.",
                "error_type": "extraction_failed"
            }

        # 6. Validar datos extraídos
        contact_data = extraction_result["data"]
        contact_validation = self.contact_validator.validate(contact_data)

        if not contact_validation["valid"]:
            self.failed_attempts[user_id] += 1
            logger.warning(
                "contact_validation_failed",
                user_id=user_id,
                error=contact_validation.get("error"),
                missing_fields=contact_validation.get("missing_fields", [])
            )

            return {
                "success": False,
                "error": contact_validation["error"],
                "error_type": "invalid_contact_data",
                "missing_fields": contact_validation.get("missing_fields", [])
            }

        # Resetear contador de intentos fallidos
        self.failed_attempts[user_id] = 0

        logger.info(
            "request_processed_successfully",
            user_id=user_id,
            contact_nombre=contact_data["nombre"]
        )

        return {
            "success": True,
            "contact": contact_data
        }

    def _validate_origin(
        self,
        user_id: int,
        username: str = None
    ) -> Dict[str, Any]:
        """
        Valida que el usuario esté autorizado.

        Args:
            user_id: ID del usuario de Telegram.
            username: Username de Telegram (opcional).

        Returns:
            dict con valid y error (si aplica).
        """
        # Verificar si está bloqueado
        if user_id in self.blocked_users:
            security_logger.log_access_attempt(
                user_id=user_id,
                authorized=False,
                username=username
            )

            logger.warning(
                "blocked_user_attempt",
                user_id=user_id,
                username=username
            )

            return {
                "valid": False,
                "error": "Usuario bloqueado. Contacta al administrador."
            }

        # Verificar si está en whitelist
        if user_id not in self.allowed_users:
            security_logger.log_access_attempt(
                user_id=user_id,
                authorized=False,
                username=username
            )

            # Incrementar intentos fallidos
            self.failed_attempts[user_id] += 1

            # Bloquear si excede intentos
            if self.failed_attempts[user_id] >= self.max_failed_attempts:
                self.blocked_users.add(user_id)
                security_logger.log_user_blocked(
                    user_id=user_id,
                    reason=f"{self.max_failed_attempts} intentos fallidos"
                )

            logger.warning(
                "unauthorized_user",
                user_id=user_id,
                username=username,
                failed_attempts=self.failed_attempts[user_id]
            )

            return {
                "valid": False,
                "error": "No tienes autorización para usar este bot."
            }

        # Usuario autorizado
        security_logger.log_access_attempt(
            user_id=user_id,
            authorized=True,
            username=username
        )

        return {"valid": True}

    def _check_rate_limit(
        self,
        user_id: int,
        username: str = None
    ) -> Dict[str, Any]:
        """
        Verifica el rate limit del usuario.

        Args:
            user_id: ID del usuario de Telegram.
            username: Username de Telegram (opcional).

        Returns:
            dict con valid y error (si aplica).
        """
        if not self.rate_limiter.is_allowed(user_id):
            security_logger.log_rate_limit_exceeded(
                user_id=user_id,
                username=username
            )

            time_until_reset = self.rate_limiter.get_time_until_reset(user_id)

            return {
                "valid": False,
                "error": f"Has excedido el límite de mensajes. Intenta en {int(time_until_reset)} segundos."
            }

        return {"valid": True}

    def add_user(self, user_id: int) -> None:
        """
        Agrega un usuario a la whitelist.

        Args:
            user_id: ID del usuario de Telegram.
        """
        self.allowed_users.add(user_id)
        logger.info("user_added_to_whitelist", user_id=user_id)

    def remove_user(self, user_id: int) -> None:
        """
        Remueve un usuario de la whitelist.

        Args:
            user_id: ID del usuario de Telegram.
        """
        self.allowed_users.discard(user_id)
        logger.info("user_removed_from_whitelist", user_id=user_id)

    def block_user(self, user_id: int) -> None:
        """
        Bloquea un usuario.

        Args:
            user_id: ID del usuario de Telegram.
        """
        self.blocked_users.add(user_id)
        security_logger.log_user_blocked(user_id=user_id, reason="manual_block")

    def unblock_user(self, user_id: int) -> None:
        """
        Desbloquea un usuario.

        Args:
            user_id: ID del usuario de Telegram.
        """
        self.blocked_users.discard(user_id)
        self.failed_attempts[user_id] = 0
        logger.info("user_unblocked", user_id=user_id)

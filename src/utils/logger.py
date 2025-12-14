"""
Sistema de logging estructurado.

Este módulo configura el logging del sistema usando structlog
para logs en formato JSON.
"""

import logging
import sys
from typing import Any
import structlog


def configure_logging(log_level: str = "INFO", log_format: str = "json") -> None:
    """
    Configura el sistema de logging estructurado.

    Args:
        log_level: Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_format: Formato de salida ('json' o 'console').
    """
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper(), logging.INFO),
    )

    processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
    ]

    if log_format == "json":
        processors.append(structlog.processors.JSONRenderer())
    else:
        processors.append(structlog.dev.ConsoleRenderer())

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, log_level.upper(), logging.INFO)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """
    Obtiene un logger estructurado.

    Args:
        name: Nombre del logger (generalmente __name__ del módulo).

    Returns:
        Logger estructurado configurado.

    Example:
        >>> logger = get_logger(__name__)
        >>> logger.info("mensaje_procesado", user_id=123, duration_ms=250)
    """
    return structlog.get_logger(name)


class SecurityLogger:
    """
    Logger especializado para eventos de seguridad.

    Attributes:
        logger: Logger estructurado base.
    """

    def __init__(self):
        """Inicializa el logger de seguridad."""
        self.logger = get_logger("security")

    def log_access_attempt(
        self,
        user_id: int,
        authorized: bool,
        username: str = None,
        chat_id: int = None
    ) -> None:
        """
        Registra un intento de acceso al sistema.

        Args:
            user_id: ID del usuario de Telegram.
            authorized: Si el acceso fue autorizado.
            username: Username de Telegram (opcional).
            chat_id: ID del chat (opcional).
        """
        self.logger.info(
            "access_attempt",
            user_id=user_id,
            authorized=authorized,
            username=username,
            chat_id=chat_id
        )

    def log_rate_limit_exceeded(self, user_id: int, username: str = None) -> None:
        """
        Registra cuando un usuario excede el rate limit.

        Args:
            user_id: ID del usuario de Telegram.
            username: Username de Telegram (opcional).
        """
        self.logger.warning(
            "rate_limit_exceeded",
            user_id=user_id,
            username=username
        )

    def log_suspicious_input(
        self,
        user_id: int,
        input_type: str,
        details: str = None
    ) -> None:
        """
        Registra entrada sospechosa detectada.

        Args:
            user_id: ID del usuario de Telegram.
            input_type: Tipo de entrada sospechosa.
            details: Detalles adicionales.
        """
        self.logger.warning(
            "suspicious_input",
            user_id=user_id,
            input_type=input_type,
            details=details
        )

    def log_user_blocked(self, user_id: int, reason: str) -> None:
        """
        Registra cuando un usuario es bloqueado.

        Args:
            user_id: ID del usuario bloqueado.
            reason: Razón del bloqueo.
        """
        self.logger.warning(
            "user_blocked",
            user_id=user_id,
            reason=reason
        )

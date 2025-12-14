"""
Sistema de rate limiting.

Este módulo implementa un rate limiter basado en ventana deslizante
para controlar la frecuencia de requests por usuario.
"""

from collections import defaultdict
from time import time
from typing import Dict, List

from .logger import get_logger

logger = get_logger(__name__)


class RateLimiter:
    """
    Rate limiter basado en ventana deslizante.

    Attributes:
        max_requests: Número máximo de requests permitidos por ventana.
        window_seconds: Duración de la ventana en segundos.
        requests: Diccionario que almacena timestamps de requests por usuario.
    """

    def __init__(self, max_requests: int = 10, window_seconds: int = 60):
        """
        Inicializa el rate limiter.

        Args:
            max_requests: Máximo de requests por ventana (default: 10).
            window_seconds: Duración de la ventana en segundos (default: 60).

        Example:
            >>> limiter = RateLimiter(max_requests=10, window_seconds=60)
            >>> if limiter.is_allowed(user_id=123):
            ...     process_request()
        """
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[int, List[float]] = defaultdict(list)

        logger.info(
            "rate_limiter_initialized",
            max_requests=max_requests,
            window_seconds=window_seconds
        )

    def is_allowed(self, user_id: int) -> bool:
        """
        Verifica si el usuario puede realizar un nuevo request.

        Args:
            user_id: ID del usuario de Telegram.

        Returns:
            True si el request está permitido, False si excede el límite.

        Example:
            >>> limiter = RateLimiter(max_requests=2, window_seconds=10)
            >>> limiter.is_allowed(123)  # Primera llamada
            True
            >>> limiter.is_allowed(123)  # Segunda llamada
            True
            >>> limiter.is_allowed(123)  # Tercera llamada (excede límite)
            False
        """
        now = time()
        window_start = now - self.window_seconds

        # Limpiar requests antiguos fuera de la ventana
        self.requests[user_id] = [
            timestamp
            for timestamp in self.requests[user_id]
            if timestamp > window_start
        ]

        # Verificar si se excede el límite
        if len(self.requests[user_id]) >= self.max_requests:
            logger.debug(
                "rate_limit_exceeded",
                user_id=user_id,
                current_requests=len(self.requests[user_id]),
                max_requests=self.max_requests
            )
            return False

        # Registrar nuevo request
        self.requests[user_id].append(now)

        logger.debug(
            "rate_limit_check",
            user_id=user_id,
            current_requests=len(self.requests[user_id]),
            max_requests=self.max_requests,
            allowed=True
        )

        return True

    def get_remaining_requests(self, user_id: int) -> int:
        """
        Obtiene el número de requests restantes para un usuario.

        Args:
            user_id: ID del usuario de Telegram.

        Returns:
            Número de requests restantes en la ventana actual.
        """
        now = time()
        window_start = now - self.window_seconds

        # Limpiar requests antiguos
        self.requests[user_id] = [
            timestamp
            for timestamp in self.requests[user_id]
            if timestamp > window_start
        ]

        current_count = len(self.requests[user_id])
        remaining = max(0, self.max_requests - current_count)

        return remaining

    def reset_user(self, user_id: int) -> None:
        """
        Resetea el contador de requests para un usuario.

        Args:
            user_id: ID del usuario de Telegram.
        """
        if user_id in self.requests:
            del self.requests[user_id]
            logger.info("rate_limit_reset", user_id=user_id)

    def get_time_until_reset(self, user_id: int) -> float:
        """
        Obtiene el tiempo en segundos hasta que se resetee el límite.

        Args:
            user_id: ID del usuario de Telegram.

        Returns:
            Segundos hasta que expire el request más antiguo.
        """
        if user_id not in self.requests or not self.requests[user_id]:
            return 0.0

        now = time()
        oldest_request = min(self.requests[user_id])
        time_until_reset = (oldest_request + self.window_seconds) - now

        return max(0.0, time_until_reset)

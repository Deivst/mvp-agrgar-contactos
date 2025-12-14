"""
Configuración centralizada del sistema.

Este módulo gestiona todas las variables de entorno y configuraciones
del sistema de gestión de contactos.
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuración del sistema basada en Pydantic Settings.

    Lee variables de entorno desde archivo .env y valida tipos.
    """

    # ========================================
    # TELEGRAM CONFIGURATION
    # ========================================
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_ALLOWED_USERS: str = ""  # Lista separada por comas

    # ========================================
    # GOOGLE GEMINI CONFIGURATION
    # ========================================
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-1.5-flash"
    GEMINI_TIMEOUT: int = 30

    # ========================================
    # DATABASE CONFIGURATION (PostgreSQL)
    # ========================================
    DATABASE_URL: str = "postgresql://user:pass@localhost:5432/contacts_db"

    # ========================================
    # CONTACTS API CONFIGURATION (Legacy support)
    # ========================================
    CONTACTS_API_URL: str = ""
    CONTACTS_API_KEY: str = ""
    CONTACTS_API_TIMEOUT: int = 10

    # ========================================
    # SECURITY CONFIGURATION
    # ========================================
    RATE_LIMIT_REQUESTS: int = 10
    RATE_LIMIT_WINDOW: int = 60  # segundos

    # ========================================
    # LOGGING CONFIGURATION
    # ========================================
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    # ========================================
    # GENERAL CONFIGURATION
    # ========================================
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

    def get_allowed_users(self) -> List[int]:
        """
        Convierte la lista de usuarios autorizados de string a lista de integers.

        Returns:
            Lista de user IDs autorizados.

        Example:
            >>> settings.TELEGRAM_ALLOWED_USERS = "123456789,987654321"
            >>> settings.get_allowed_users()
            [123456789, 987654321]
        """
        if not self.TELEGRAM_ALLOWED_USERS:
            return []

        try:
            return [
                int(user_id.strip())
                for user_id in self.TELEGRAM_ALLOWED_USERS.split(",")
                if user_id.strip()
            ]
        except ValueError:
            return []


# Instancia global de configuración
settings = Settings()

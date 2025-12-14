#!/usr/bin/env python3
"""
Script de inicialización de base de datos PostgreSQL.

Este script crea las tablas necesarias usando SQLAlchemy ORM.
"""

import sys
from pathlib import Path

# Agregar directorio raíz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from src.services.contacts_api import ContactsAPIClient
from config.settings import settings
from src.utils.logger import configure_logging, get_logger

configure_logging(log_level="INFO", log_format="console")
logger = get_logger(__name__)


def init_database():
    """Inicializa la base de datos creando las tablas necesarias."""
    logger.info(
        "initializing_database",
        database_url=settings.DATABASE_URL.split("@")[-1]
    )

    try:
        # Crear cliente
        client = ContactsAPIClient(database_url=settings.DATABASE_URL)

        # Crear tablas
        client.create_tables()

        logger.info("database_initialized_successfully")

        print("\n✅ Base de datos inicializada correctamente!")
        print(f"📍 URL: {settings.DATABASE_URL.split('@')[-1]}")
        print("\nTablas creadas:")
        print("  - contacts")

        return True

    except Exception as e:
        logger.error("failed_to_initialize_database", error=str(e))
        print(f"\n❌ Error al inicializar base de datos: {e}")
        return False


if __name__ == "__main__":
    success = init_database()
    sys.exit(0 if success else 1)

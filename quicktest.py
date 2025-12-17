#!/usr/bin/env python
"""
Script de prueba rápida - Valida que todos los componentes funcionen
sin necesidad de BD PostgreSQL real (usa SQLite para testing).
"""

import sys
import os

# Agregar src al path
sys.path.insert(0, os.path.dirname(__file__))

async def test_components():
    """Prueba que todos los componentes principales se pueden importar y inicializar."""
    print("=" * 70)
    print("PRUEBA DE COMPONENTES - Sistema Multi-Agente de Gestión de Contactos")
    print("=" * 70)
    
    try:
        # Test 1: Cargar configuración
        print("\n[1/5] Cargando configuración...")
        from config.settings import settings
        print(f"    ✓ Configuración cargada")
        print(f"    - Token Telegram: {settings.TELEGRAM_BOT_TOKEN[:20]}...")
        print(f"    - Gemini API Key: {settings.GEMINI_API_KEY[:20]}...")
        print(f"    - Base de datos: {settings.DATABASE_URL}")
        
        # Test 2: Logger
        print("\n[2/5] Inicializando logger...")
        from src.utils.logger import configure_logging, get_logger
        configure_logging(log_level="INFO", log_format="console")
        logger = get_logger(__name__)
        logger.info("Logger inicializado correctamente")
        print("    ✓ Logger configurado")
        
        # Test 3: Servicios
        print("\n[3/5] Inicializando servicios...")
        from src.services.gemini_service import GeminiService
        from src.services.telegram_service import TelegramService
        
        gemini_service = GeminiService(api_key=settings.GEMINI_API_KEY, model=settings.GEMINI_MODEL)
        print("    ✓ GeminiService inicializado")
        
        telegram_service = TelegramService()
        print("    ✓ TelegramService inicializado")
        
        # Test 4: Agentes
        print("\n[4/5] Inicializando agentes...")
        from src.agents.security_agent import SecurityAgent
        from src.agents.persistence_agent import PersistenceAgent
        
        security_agent = SecurityAgent()
        print("    ✓ SecurityAgent inicializado")
        
        persistence_agent = PersistenceAgent()
        print("    ✓ PersistenceAgent inicializado")
        
        # Test 5: Validadores
        print("\n[5/5] Cargando validadores...")
        from src.validators.contact_validator import ContactValidator
        from src.validators.message_validator import MessageValidator
        
        contact_validator = ContactValidator()
        message_validator = MessageValidator()
        print("    ✓ Validadores inicializados")
        
        print("\n" + "=" * 70)
        print("✓ TODAS LAS PRUEBAS PASARON CORRECTAMENTE")
        print("=" * 70)
        print("\nPróximos pasos:")
        print("1. Verificar que PostgreSQL está ejecutándose")
        print("2. Ejecutar: python scripts/init_db.py")
        print("3. Ejecutar: python main.py")
        print("\nO si usas Docker:")
        print("1. docker-compose up -d")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import asyncio
    success = asyncio.run(test_components())
    sys.exit(0 if success else 1)

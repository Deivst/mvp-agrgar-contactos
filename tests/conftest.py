"""
Configuración compartida de pytest.

Este módulo contiene fixtures reutilizables para todos los tests.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from src.models.contact import Contact
from src.services.gemini_service import GeminiService
from src.agents.security_agent import SecurityAgent


@pytest.fixture
def sample_contact_data():
    """Fixture con datos de ejemplo para un contacto."""
    return {
        "nombre": "Juan Pérez",
        "telefono": "3001234567",
        "quien_lo_recomendo": "María López"
    }


@pytest.fixture
def sample_contact(sample_contact_data):
    """Fixture con una instancia de Contact."""
    return Contact(**sample_contact_data)


@pytest.fixture
def sample_telegram_message():
    """Fixture con un mensaje de Telegram de ejemplo."""
    return {
        "text": "Juan Pérez 3001234567 recomendado por María López",
        "user_id": 123456789,
        "chat_id": 987654321,
        "username": "testuser"
    }


@pytest.fixture
def mock_gemini_service():
    """Fixture con un mock de GeminiService."""
    mock = MagicMock(spec=GeminiService)
    mock.extract_contact_info = AsyncMock()
    mock.health_check = AsyncMock(return_value=True)
    return mock


@pytest.fixture
def mock_gemini_response_success():
    """Fixture con una respuesta exitosa de Gemini."""
    return {
        "success": True,
        "data": {
            "nombre": "Juan Pérez",
            "telefono": "3001234567",
            "quien_lo_recomendo": "María López"
        }
    }


@pytest.fixture
def mock_gemini_response_failure():
    """Fixture con una respuesta fallida de Gemini."""
    return {
        "success": False,
        "error": "Error al procesar con Gemini"
    }

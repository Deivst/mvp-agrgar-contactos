"""
Tests unitarios para los validadores.
"""

import pytest

from src.validators.message_validator import MessageValidator
from src.validators.contact_validator import ContactValidator


class TestMessageValidator:
    """Tests para MessageValidator."""

    @pytest.fixture
    def validator(self):
        """Fixture que provee una instancia del validador."""
        return MessageValidator()

    def test_should_validate_valid_message(self, validator, sample_telegram_message):
        """Verifica validación exitosa de mensaje válido."""
        # Act
        result = validator.validate(sample_telegram_message)

        # Assert
        assert result["valid"] is True
        assert "message" in result

    def test_should_reject_empty_message(self, validator):
        """Verifica rechazo de mensaje vacío."""
        # Arrange
        message = {
            "text": "",
            "user_id": 123,
            "chat_id": 456
        }

        # Act
        result = validator.validate(message)

        # Assert
        assert result["valid"] is False
        assert "vacío" in result["error"].lower()

    def test_should_reject_short_message(self, validator):
        """Verifica rechazo de mensaje muy corto."""
        # Arrange
        message = {
            "text": "Hi",
            "user_id": 123,
            "chat_id": 456
        }

        # Act
        result = validator.validate(message)

        # Assert
        assert result["valid"] is False
        assert "corto" in result["error"].lower()

    def test_should_reject_message_without_required_fields(self, validator):
        """Verifica rechazo de mensaje sin campos requeridos."""
        # Arrange
        message = {
            "text": "Texto válido"
            # Falta user_id y chat_id
        }

        # Act
        result = validator.validate(message)

        # Assert
        assert result["valid"] is False
        assert "requerido" in result["error"].lower()


class TestContactValidator:
    """Tests para ContactValidator."""

    @pytest.fixture
    def validator(self):
        """Fixture que provee una instancia del validador."""
        return ContactValidator()

    def test_should_validate_valid_contact(self, validator, sample_contact_data):
        """Verifica validación exitosa de contacto válido."""
        # Act
        result = validator.validate(sample_contact_data)

        # Assert
        assert result["valid"] is True
        assert "data" in result

    def test_should_reject_contact_without_name(self, validator):
        """Verifica rechazo de contacto sin nombre."""
        # Arrange
        contact_data = {
            "telefono": "3001234567",
            "quien_lo_recomendo": "María"
        }

        # Act
        result = validator.validate(contact_data)

        # Assert
        assert result["valid"] is False
        assert "nombre" in result.get("missing_fields", [])

    def test_should_reject_contact_with_empty_fields(self, validator):
        """Verifica rechazo de contacto con campos vacíos."""
        # Arrange
        contact_data = {
            "nombre": "",
            "telefono": "3001234567",
            "quien_lo_recomendo": "María"
        }

        # Act
        result = validator.validate(contact_data)

        # Assert
        assert result["valid"] is False
        assert "vacío" in result["error"].lower()

    def test_should_reject_phone_too_short(self, validator):
        """Verifica rechazo de teléfono muy corto."""
        # Arrange
        contact_data = {
            "nombre": "Juan",
            "telefono": "123",
            "quien_lo_recomendo": "María"
        }

        # Act
        result = validator.validate(contact_data)

        # Assert
        assert result["valid"] is False
        assert "10 dígitos" in result["error"]

    def test_should_reject_phone_too_long(self, validator):
        """Verifica rechazo de teléfono muy largo."""
        # Arrange
        contact_data = {
            "nombre": "Juan",
            "telefono": "1234567890123456",  # 16 dígitos
            "quien_lo_recomendo": "María"
        }

        # Act
        result = validator.validate(contact_data)

        # Assert
        assert result["valid"] is False
        assert "15 dígitos" in result["error"]

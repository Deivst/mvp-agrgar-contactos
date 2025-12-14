"""
Tests unitarios para el modelo Contact.
"""

import pytest
from pydantic import ValidationError

from src.models.contact import Contact


class TestContact:
    """Tests para el modelo Contact."""

    def test_should_create_contact_when_all_fields_valid(self, sample_contact_data):
        """Verifica creación exitosa con todos los campos válidos."""
        # Act
        contact = Contact(**sample_contact_data)

        # Assert
        assert contact.nombre == "Juan Pérez"
        assert contact.telefono == "+573001234567"
        assert contact.quien_lo_recomendo == "María López"
        assert contact.source == "telegram"

    def test_should_normalize_phone_when_has_spaces(self):
        """Verifica normalización de teléfono con espacios."""
        # Act
        contact = Contact(
            nombre="Test",
            telefono="300 123 4567",
            quien_lo_recomendo="Ref"
        )

        # Assert
        assert contact.telefono == "+573001234567"

    def test_should_normalize_phone_when_has_dashes(self):
        """Verifica normalización de teléfono con guiones."""
        # Act
        contact = Contact(
            nombre="Test",
            telefono="300-123-4567",
            quien_lo_recomendo="Ref"
        )

        # Assert
        assert contact.telefono == "+573001234567"

    def test_should_add_country_code_when_missing(self):
        """Verifica que se agrega código de país +57 si falta."""
        # Act
        contact = Contact(
            nombre="Test",
            telefono="3001234567",
            quien_lo_recomendo="Ref"
        )

        # Assert
        assert contact.telefono.startswith("+57")

    def test_should_raise_error_when_phone_too_short(self):
        """Verifica error cuando teléfono tiene menos de 10 dígitos."""
        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            Contact(
                nombre="Test",
                telefono="12345",
                quien_lo_recomendo="Ref"
            )

        assert "10 dígitos" in str(exc_info.value)

    def test_should_raise_error_when_phone_too_long(self):
        """Verifica error cuando teléfono tiene más de 15 dígitos."""
        # Act & Assert
        with pytest.raises(ValidationError):
            Contact(
                nombre="Test",
                telefono="1234567890123456",  # 16 dígitos
                quien_lo_recomendo="Ref"
            )

    def test_should_clean_extra_spaces_in_name(self):
        """Verifica que se limpian espacios extras en nombre."""
        # Act
        contact = Contact(
            nombre="  Juan   Carlos   Pérez  ",
            telefono="3001234567",
            quien_lo_recomendo="Ref"
        )

        # Assert
        assert contact.nombre == "Juan Carlos Pérez"

    def test_should_raise_error_when_name_empty(self):
        """Verifica error cuando nombre está vacío."""
        # Act & Assert
        with pytest.raises(ValidationError):
            Contact(
                nombre="",
                telefono="3001234567",
                quien_lo_recomendo="María"
            )

    def test_should_raise_error_when_name_only_spaces(self):
        """Verifica error cuando nombre contiene solo espacios."""
        # Act & Assert
        with pytest.raises(ValidationError):
            Contact(
                nombre="   ",
                telefono="3001234567",
                quien_lo_recomendo="Ref"
            )

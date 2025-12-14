"""
Validador de datos de contacto.

Este módulo valida los datos extraídos de contactos
antes de persistirlos.
"""

from typing import Dict, Any, List
from ..utils.logger import get_logger

logger = get_logger(__name__)


class ContactValidator:
    """
    Validador de datos de contacto.

    Valida que los datos extraídos por Gemini sean completos
    y cumplan con los requerimientos del sistema.
    """

    REQUIRED_FIELDS = ["nombre", "telefono", "quien_lo_recomendo"]

    def validate(self, contact_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida los datos de un contacto.

        Args:
            contact_data: Diccionario con datos del contacto.
                Expected keys: nombre, telefono, quien_lo_recomendo

        Returns:
            dict con keys:
                - valid: bool
                - error: str (si valid=False)
                - missing_fields: list (campos faltantes si valid=False)
                - data: dict (datos validados si valid=True)

        Example:
            >>> validator = ContactValidator()
            >>> result = validator.validate({
            ...     "nombre": "Juan Pérez",
            ...     "telefono": "3001234567",
            ...     "quien_lo_recomendo": "María"
            ... })
            >>> result["valid"]
            True
        """
        # Verificar campos requeridos
        missing_fields = self._check_required_fields(contact_data)

        if missing_fields:
            logger.warning(
                "missing_contact_fields",
                missing_fields=missing_fields,
                provided_fields=list(contact_data.keys())
            )
            return {
                "valid": False,
                "error": f"Campos faltantes: {', '.join(missing_fields)}",
                "missing_fields": missing_fields
            }

        # Validar que los campos no estén vacíos
        empty_fields = self._check_empty_fields(contact_data)

        if empty_fields:
            logger.warning(
                "empty_contact_fields",
                empty_fields=empty_fields
            )
            return {
                "valid": False,
                "error": f"Los siguientes campos están vacíos: {', '.join(empty_fields)}",
                "missing_fields": empty_fields
            }

        # Validar formato de nombre
        nombre_validation = self._validate_nombre(contact_data["nombre"])
        if not nombre_validation["valid"]:
            return nombre_validation

        # Validar formato de teléfono
        telefono_validation = self._validate_telefono(contact_data["telefono"])
        if not telefono_validation["valid"]:
            return telefono_validation

        # Validar referido
        referido_validation = self._validate_referido(contact_data["quien_lo_recomendo"])
        if not referido_validation["valid"]:
            return referido_validation

        logger.debug(
            "contact_validation_passed",
            nombre=contact_data["nombre"]
        )

        return {
            "valid": True,
            "data": contact_data
        }

    def _check_required_fields(self, data: Dict[str, Any]) -> List[str]:
        """
        Verifica que existan todos los campos requeridos.

        Args:
            data: Diccionario con datos a validar.

        Returns:
            Lista de campos faltantes (vacía si todos están presentes).
        """
        missing = []
        for field in self.REQUIRED_FIELDS:
            if field not in data:
                missing.append(field)
        return missing

    def _check_empty_fields(self, data: Dict[str, Any]) -> List[str]:
        """
        Verifica que los campos requeridos no estén vacíos.

        Args:
            data: Diccionario con datos a validar.

        Returns:
            Lista de campos vacíos.
        """
        empty = []
        for field in self.REQUIRED_FIELDS:
            value = data.get(field, "")
            if not value or not str(value).strip():
                empty.append(field)
        return empty

    def _validate_nombre(self, nombre: str) -> Dict[str, Any]:
        """
        Valida el campo nombre.

        Args:
            nombre: Nombre a validar.

        Returns:
            dict con valid y error (si aplica).
        """
        nombre = nombre.strip()

        if len(nombre) < 2:
            return {
                "valid": False,
                "error": "El nombre debe tener al menos 2 caracteres"
            }

        if len(nombre) > 255:
            return {
                "valid": False,
                "error": "El nombre no puede exceder 255 caracteres"
            }

        return {"valid": True}

    def _validate_telefono(self, telefono: str) -> Dict[str, Any]:
        """
        Valida el campo teléfono.

        Args:
            telefono: Teléfono a validar.

        Returns:
            dict con valid y error (si aplica).
        """
        import re

        # Remover todo excepto dígitos y +
        digits_only = re.sub(r'[^\d]', '', telefono)

        if len(digits_only) < 10:
            return {
                "valid": False,
                "error": f"El teléfono debe tener al menos 10 dígitos (encontrados: {len(digits_only)})"
            }

        if len(digits_only) > 15:
            return {
                "valid": False,
                "error": f"El teléfono no puede tener más de 15 dígitos (encontrados: {len(digits_only)})"
            }

        return {"valid": True}

    def _validate_referido(self, referido: str) -> Dict[str, Any]:
        """
        Valida el campo quien_lo_recomendo.

        Args:
            referido: Nombre del referido a validar.

        Returns:
            dict con valid y error (si aplica).
        """
        referido = referido.strip()

        if len(referido) < 2:
            return {
                "valid": False,
                "error": "El nombre del referido debe tener al menos 2 caracteres"
            }

        if len(referido) > 255:
            return {
                "valid": False,
                "error": "El nombre del referido no puede exceder 255 caracteres"
            }

        return {"valid": True}

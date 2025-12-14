"""
Funciones auxiliares y utilidades generales.

Este módulo contiene funciones helper utilizadas en todo el sistema.
"""

import re
import html
from typing import Optional
from io import BytesIO

from .logger import get_logger

logger = get_logger(__name__)


class DataSanitizer:
    """
    Sanitizador de datos de entrada.

    Implementa sanitización de inputs siguiendo guías de OWASP
    para prevenir inyección de código y otros ataques.
    """

    # Patrones peligrosos a detectar
    DANGEROUS_PATTERNS = [
        r'<script.*?>.*?</script>',  # Scripts
        r'javascript:',               # JavaScript protocol
        r'on\w+\s*=',                # Event handlers (onclick, onerror, etc.)
        r'\$\{.*?\}',                # Template injection
        r'\{\{.*?\}\}',              # Jinja/Mustache templates
        r'<iframe',                  # iframes
        r'<object',                  # objects
        r'<embed',                   # embeds
    ]

    @classmethod
    def sanitize(cls, text: str) -> str:
        """
        Sanitiza texto de entrada.

        Args:
            text: Texto a sanitizar.

        Returns:
            Texto sanitizado.

        Example:
            >>> DataSanitizer.sanitize("<script>alert('xss')</script>Juan")
            "Juan"
        """
        if not text:
            return ""

        # HTML escape para prevenir XSS
        sanitized = html.escape(text)

        # Remover patrones peligrosos
        for pattern in cls.DANGEROUS_PATTERNS:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)

        # Limitar longitud para prevenir DoS
        sanitized = sanitized[:1000]

        return sanitized.strip()

    @classmethod
    def is_safe(cls, text: str) -> bool:
        """
        Verifica si el texto contiene patrones peligrosos.

        Args:
            text: Texto a verificar.

        Returns:
            True si el texto es seguro, False si contiene patrones peligrosos.
        """
        if not text:
            return True

        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                logger.warning(
                    "dangerous_pattern_detected",
                    pattern=pattern,
                    text_preview=text[:50]
                )
                return False

        return True


def generate_vcard(nombre: str, telefono: str, quien_lo_recomendo: str) -> str:
    """
    Genera un archivo vCard (VCF) para un contacto.

    Args:
        nombre: Nombre completo del contacto.
        telefono: Número de teléfono normalizado.
        quien_lo_recomendo: Nombre de quien recomendó el contacto.

    Returns:
        Contenido del archivo vCard en formato string.

    Example:
        >>> vcard = generate_vcard("Juan Pérez", "+573001234567", "María")
        >>> print(vcard)
        BEGIN:VCARD
        VERSION:3.0
        FN:Juan Pérez
        TEL;TYPE=CELL:+573001234567
        NOTE:Recomendado por: María
        END:VCARD
    """
    vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{nombre}
TEL;TYPE=CELL:{telefono}
NOTE:Recomendado por: {quien_lo_recomendo}
END:VCARD"""

    logger.debug(
        "vcard_generated",
        nombre=nombre,
        telefono=telefono
    )

    return vcard


def vcard_to_bytes(vcard: str) -> BytesIO:
    """
    Convierte un vCard string a BytesIO para enviar por Telegram.

    Args:
        vcard: Contenido del vCard en formato string.

    Returns:
        BytesIO con el contenido del vCard.

    Example:
        >>> vcard = generate_vcard("Juan", "+573001234567", "María")
        >>> vcard_bytes = vcard_to_bytes(vcard)
        >>> # vcard_bytes se puede enviar como archivo en Telegram
    """
    return BytesIO(vcard.encode('utf-8'))


def normalize_phone_for_telegram(telefono: str) -> str:
    """
    Normaliza teléfono para el botón de compartir de Telegram.

    Telegram requiere el número sin el símbolo +.

    Args:
        telefono: Número de teléfono (puede incluir +).

    Returns:
        Número sin el símbolo +.

    Example:
        >>> normalize_phone_for_telegram("+573001234567")
        "573001234567"
    """
    return telefono.replace("+", "")


def format_contact_message(
    nombre: str,
    telefono: str,
    quien_lo_recomendo: str,
    contact_id: Optional[str] = None
) -> str:
    """
    Formatea un mensaje de confirmación de contacto guardado.

    Args:
        nombre: Nombre del contacto.
        telefono: Teléfono del contacto.
        quien_lo_recomendo: Nombre del referido.
        contact_id: ID del contacto en base de datos (opcional).

    Returns:
        Mensaje formateado para enviar al usuario.

    Example:
        >>> msg = format_contact_message("Juan", "+573001234567", "María", "uuid-123")
        >>> print(msg)
        ✅ Contacto guardado exitosamente:
        <BLANKLINE>
        👤 Nombre: Juan
        📱 Teléfono: +573001234567
        🤝 Recomendado por: María
    """
    message = f"""✅ Contacto guardado exitosamente:

👤 Nombre: {nombre}
📱 Teléfono: {telefono}
🤝 Recomendado por: {quien_lo_recomendo}"""

    if contact_id:
        message += f"\n\n🆔 ID: {contact_id}"

    return message


def format_error_message(error: str, details: Optional[str] = None) -> str:
    """
    Formatea un mensaje de error para el usuario.

    Args:
        error: Mensaje de error principal.
        details: Detalles adicionales del error (opcional).

    Returns:
        Mensaje de error formateado.

    Example:
        >>> msg = format_error_message("Campo faltante", "El teléfono es requerido")
        >>> print(msg)
        ❌ Error: Campo faltante
        <BLANKLINE>
        Detalles: El teléfono es requerido
    """
    message = f"❌ Error: {error}"

    if details:
        message += f"\n\nDetalles: {details}"

    return message


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Trunca un texto a una longitud máxima.

    Args:
        text: Texto a truncar.
        max_length: Longitud máxima (default: 100).

    Returns:
        Texto truncado con "..." al final si es necesario.

    Example:
        >>> truncate_text("Este es un texto muy largo", 10)
        "Este es..."
    """
    if len(text) <= max_length:
        return text

    return text[:max_length - 3] + "..."

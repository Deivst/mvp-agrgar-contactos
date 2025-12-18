"""
Fixtures comunes para tests
"""
import pytest
import numpy as np
from pathlib import Path

from src.core.config import Config


@pytest.fixture
def sample_config():
    """Configuracion de prueba"""
    return Config()


@pytest.fixture
def sample_image():
    """Imagen de prueba (blanca con texto negro simulado)"""
    # Crear imagen blanca 1000x800
    image = np.ones((800, 1000, 3), dtype=np.uint8) * 255
    return image


@pytest.fixture
def sample_ocr_text():
    """Texto OCR de ejemplo para un albaran"""
    return """
    ALBARAN DE ENTREGA

    Numero: ALB-20250115
    Fecha: 15/01/2025

    PROVEEDOR:
    Distribuciones Lopez S.L.
    CIF: B12345678
    Calle Mayor 123, Madrid

    CLIENTE:
    Farmacia Garcia
    CIF: B87654321
    Avenida Principal 45, Barcelona

    PRODUCTOS:
    Codigo     Descripcion              Cantidad    Precio    Subtotal
    MED-001    Paracetamol 500mg x100   50          4.50      225.00
    MED-002    Ibuprofeno 600mg x50     30          6.80      204.00

    TOTAL: 429.00 EUR

    Firma del transportista: [X]
    Sello de empresa: [X]
    """


@pytest.fixture
def temp_output_dir(tmp_path):
    """Directorio temporal para salidas de test"""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir

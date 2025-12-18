"""
Tests para modelos Pydantic
"""
import pytest
from datetime import date
from pydantic import ValidationError

from src.models.document import BBox, OCRResult, DocumentType
from src.models.fields import Producto, Proveedor, Cliente
from src.models.schemas import AlbaranSchema


def test_bbox_valid():
    """Test creacion de BBox valido"""
    bbox = BBox(x1=10, y1=20, x2=100, y2=200)
    assert bbox.x1 == 10
    assert bbox.y1 == 20
    assert bbox.x2 == 100
    assert bbox.y2 == 200
    assert bbox.area() == 90 * 180


def test_bbox_invalid_x2():
    """Test que x2 debe ser mayor que x1"""
    with pytest.raises(ValidationError):
        BBox(x1=100, y1=20, x2=10, y2=200)


def test_bbox_invalid_y2():
    """Test que y2 debe ser mayor que y1"""
    with pytest.raises(ValidationError):
        BBox(x1=10, y1=200, x2=100, y2=20)


def test_ocr_result_valid():
    """Test creacion de OCRResult valido"""
    bbox = BBox(x1=10, y1=20, x2=100, y2=50)
    ocr_result = OCRResult(
        text="Hola Mundo",
        bbox=bbox,
        confidence=0.95
    )
    assert ocr_result.text == "Hola Mundo"
    assert ocr_result.confidence == 0.95


def test_ocr_result_strips_text():
    """Test que OCRResult hace strip del texto"""
    bbox = BBox(x1=10, y1=20, x2=100, y2=50)
    ocr_result = OCRResult(
        text="  Hola Mundo  ",
        bbox=bbox,
        confidence=0.95
    )
    assert ocr_result.text == "Hola Mundo"


def test_ocr_result_empty_text():
    """Test que OCRResult rechaza texto vacio"""
    bbox = BBox(x1=10, y1=20, x2=100, y2=50)
    with pytest.raises(ValidationError):
        OCRResult(text="", bbox=bbox, confidence=0.95)


def test_producto_valid():
    """Test creacion de Producto valido"""
    producto = Producto(
        codigo_producto="MED-001",
        descripcion="Paracetamol 500mg",
        cantidad=50,
        precio_unitario=4.50,
        subtotal=225.00
    )
    assert producto.cantidad == 50
    assert producto.precio_unitario == 4.50


def test_producto_cantidad_negativa():
    """Test que cantidad debe ser positiva"""
    with pytest.raises(ValidationError):
        Producto(
            codigo_producto="MED-001",
            descripcion="Paracetamol",
            cantidad=0,
            precio_unitario=4.50
        )


def test_albaran_schema_valid():
    """Test creacion de AlbaranSchema valido"""
    albaran = AlbaranSchema(
        numero_albaran="ALB-20250115",
        fecha_emision=date(2025, 1, 15),
        proveedor=Proveedor(
            razon_social="Proveedor Test",
            cif="B12345678"
        ),
        cliente=Cliente(
            razon_social="Cliente Test",
            cif="B87654321"
        ),
        productos=[
            Producto(
                codigo_producto="P001",
                descripcion="Producto 1",
                cantidad=10,
                precio_unitario=5.0,
                subtotal=50.0
            )
        ],
        total=50.0,
        firma_transportista=True,
        sello_empresa=True
    )
    assert albaran.numero_albaran == "ALB-20250115"
    assert albaran.total == 50.0


def test_albaran_schema_invalid_numero():
    """Test que numero_albaran debe seguir el patron"""
    with pytest.raises(ValidationError):
        AlbaranSchema(
            numero_albaran="INVALID",
            fecha_emision=date(2025, 1, 15),
            proveedor=Proveedor(razon_social="Test"),
            cliente=Cliente(razon_social="Test"),
            productos=[
                Producto(
                    codigo_producto="P001",
                    descripcion="Producto 1",
                    cantidad=10
                )
            ],
            total=0
        )

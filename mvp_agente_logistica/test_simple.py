"""
Script de prueba demo simple (sin emojis para compatibilidad Windows)
No requiere Tesseract ni Ollama instalados
"""

import json
from datetime import datetime
from pathlib import Path
import sys

# Agregar src al path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from models.schemas import (
    ProcessedDocument,
    DocumentType,
    AlbaranFields,
    OrdenEnvioFields,
    ValidationResult
)
from models.fields import (
    Proveedor,
    Cliente,
    ProductoAlbaran,
    Ubicacion,
    ProductoOrden
)


def crear_albaran_ficticio():
    """Crea un albaran ficticio completo"""

    proveedor = Proveedor(
        razon_social="Distribuciones Lopez S.L.",
        cif="B12345678",
        direccion="Calle Mayor 123, Madrid"
    )

    cliente = Cliente(
        razon_social="Farmacia Garcia",
        cif="B87654321",
        direccion_entrega="Avenida Principal 45, Barcelona"
    )

    productos = [
        ProductoAlbaran(
            codigo_producto="MED-001",
            descripcion="Paracetamol 500mg x100",
            cantidad=50,
            precio_unitario=4.50,
            subtotal=225.00
        ),
        ProductoAlbaran(
            codigo_producto="MED-002",
            descripcion="Ibuprofeno 600mg x50",
            cantidad=30,
            precio_unitario=6.80,
            subtotal=204.00
        ),
        ProductoAlbaran(
            codigo_producto="MED-003",
            descripcion="Omeprazol 20mg x28",
            cantidad=25,
            precio_unitario=8.50,
            subtotal=212.50
        )
    ]

    albaran_fields = AlbaranFields(
        numero_albaran="ALB-20250117",
        fecha_emision="2025-01-17",
        proveedor=proveedor,
        cliente=cliente,
        productos=productos,
        total=641.50,
        firma_transportista=True,
        sello_empresa=True,
        observaciones="Entrega urgente - Manejar con cuidado"
    )

    validation = ValidationResult(
        status="valid",
        errors=[],
        warnings=[]
    )

    documento = ProcessedDocument(
        metadata={
            "file_path": "data/raw/albaran_demo_001.pdf",
            "file_name": "albaran_demo_001.pdf",
            "file_size_kb": 245,
            "processing_timestamp": datetime.now().isoformat(),
            "processing_time_seconds": 12.5,
            "agent_version": "1.0.0-demo"
        },
        classification={
            "document_type": DocumentType.ALBARAN,
            "confidence": 0.98,
            "alternative_types": []
        },
        ocr_info={
            "engine_used": "Demo Mode",
            "average_confidence": 0.95,
            "total_text_blocks": 42,
            "tables_detected": 1,
            "signatures_detected": True,
            "stamps_detected": True
        },
        extracted_fields=albaran_fields.model_dump(),
        validation=validation,
        raw_ocr_text="ALBARAN DE ENTREGA - ALB-20250117..."
    )

    return documento


def crear_orden_envio_ficticia():
    """Crea una orden de envio ficticia"""

    origen = Ubicacion(
        ubicacion="Almacen Central Madrid",
        direccion="Poligono Industrial Norte, Nave 5",
        codigo_postal="28001"
    )

    destino = Ubicacion(
        ubicacion="Farmacia Garcia",
        direccion="Avenida Principal 45, Barcelona",
        codigo_postal="08001"
    )

    productos = [
        ProductoOrden(
            codigo="MED-001",
            descripcion="Paracetamol 500mg x100",
            cantidad_ordenada=50,
            ubicacion_almacen="A-12-03"
        ),
        ProductoOrden(
            codigo="MED-002",
            descripcion="Ibuprofeno 600mg x50",
            cantidad_ordenada=30,
            ubicacion_almacen="A-12-05"
        )
    ]

    orden_fields = OrdenEnvioFields(
        numero_orden="ORD-20250116",
        fecha_orden="2025-01-16",
        fecha_envio_programada="2025-01-17",
        origen=origen,
        destino=destino,
        productos=productos,
        transportista="TransExpress S.A.",
        instrucciones_especiales="Requiere refrigeracion"
    )

    validation = ValidationResult(status="valid", errors=[], warnings=[])

    documento = ProcessedDocument(
        metadata={
            "file_path": "data/raw/orden_envio_demo_001.pdf",
            "file_name": "orden_envio_demo_001.pdf",
            "file_size_kb": 180,
            "processing_timestamp": datetime.now().isoformat(),
            "processing_time_seconds": 10.2,
            "agent_version": "1.0.0-demo"
        },
        classification={
            "document_type": DocumentType.ORDEN_ENVIO,
            "confidence": 0.96,
            "alternative_types": []
        },
        ocr_info={
            "engine_used": "Demo Mode",
            "average_confidence": 0.93,
            "total_text_blocks": 35,
            "tables_detected": 1,
            "signatures_detected": False,
            "stamps_detected": True
        },
        extracted_fields=orden_fields.model_dump(),
        validation=validation,
        raw_ocr_text="ORDEN DE ENVIO ORD-20250116..."
    )

    return documento


def ejecutar_prueba():
    """Ejecuta la prueba completa"""

    print("=" * 70)
    print("PRUEBA DEMO - AGENTE DE CLASIFICACION DE DOCUMENTOS LOGISTICOS")
    print("=" * 70)
    print()

    # Crear directorio de salida
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Test 1: Albaran
    print("[Test 1] Procesando ALBARAN ficticio...")
    print("-" * 70)

    albaran = crear_albaran_ficticio()

    print(f"[OK] Documento clasificado como: {albaran.classification['document_type']}")
    print(f"[OK] Confianza: {albaran.classification['confidence']*100:.1f}%")
    print(f"[OK] Motor OCR: {albaran.ocr_info['engine_used']}")
    print(f"[OK] Confianza OCR: {albaran.ocr_info['average_confidence']*100:.1f}%")
    print()

    print("Campos extraidos:")
    print(f"  - Numero albaran: {albaran.extracted_fields['numero_albaran']}")
    print(f"  - Fecha: {albaran.extracted_fields['fecha_emision']}")
    print(f"  - Proveedor: {albaran.extracted_fields['proveedor']['razon_social']}")
    print(f"  - Cliente: {albaran.extracted_fields['cliente']['razon_social']}")
    print(f"  - Total productos: {len(albaran.extracted_fields['productos'])}")
    print(f"  - Importe total: {albaran.extracted_fields['total']} EUR")
    print(f"  - Firma: {'Si' if albaran.extracted_fields['firma_transportista'] else 'No'}")
    print()

    print("Detalle de productos:")
    for i, p in enumerate(albaran.extracted_fields['productos'], 1):
        print(f"  {i}. [{p['codigo_producto']}] {p['descripcion']}")
        print(f"     Cant: {p['cantidad']} | Precio: {p['precio_unitario']} EUR | Subtotal: {p['subtotal']} EUR")
    print()

    print(f"Validacion: {albaran.validation.status.upper()}")
    print(f"  - Errores: {len(albaran.validation.errors)}")
    print(f"  - Advertencias: {len(albaran.validation.warnings)}")
    print()

    # Guardar JSON
    output_file = output_dir / "albaran_demo_001.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(albaran.model_dump(), f, indent=2, ensure_ascii=False, default=str)

    print(f"[GUARDADO] {output_file}")
    print()

    # Test 2: Orden de Envio
    print("=" * 70)
    print("[Test 2] Procesando ORDEN DE ENVIO ficticia...")
    print("-" * 70)

    orden = crear_orden_envio_ficticia()

    print(f"[OK] Documento clasificado como: {orden.classification['document_type']}")
    print(f"[OK] Confianza: {orden.classification['confidence']*100:.1f}%")
    print()

    print("Campos extraidos:")
    print(f"  - Numero orden: {orden.extracted_fields['numero_orden']}")
    print(f"  - Fecha orden: {orden.extracted_fields['fecha_orden']}")
    print(f"  - Fecha envio: {orden.extracted_fields['fecha_envio_programada']}")
    print(f"  - Origen: {orden.extracted_fields['origen']['ubicacion']}")
    print(f"  - Destino: {orden.extracted_fields['destino']['ubicacion']}")
    print(f"  - Transportista: {orden.extracted_fields['transportista']}")
    print(f"  - Total productos: {len(orden.extracted_fields['productos'])}")
    print()

    # Guardar JSON
    output_file = output_dir / "orden_envio_demo_001.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(orden.model_dump(), f, indent=2, ensure_ascii=False, default=str)

    print(f"[GUARDADO] {output_file}")
    print()

    # Resumen
    print("=" * 70)
    print("PRUEBA COMPLETADA EXITOSAMENTE")
    print("=" * 70)
    print()
    print("Resumen:")
    print(f"  - Documentos procesados: 2")
    print(f"  - Albaranes: 1")
    print(f"  - Ordenes de envio: 1")
    print(f"  - Archivos JSON generados: 2")
    print()
    print("Archivos generados en: data/processed/")
    print("  - albaran_demo_001.json")
    print("  - orden_envio_demo_001.json")
    print()
    print("[OK] El sistema funciona correctamente!")
    print("[OK] Los modelos Pydantic validan los datos")
    print("[OK] La estructura JSON es correcta")
    print()
    print("Siguiente paso:")
    print("  Instalar Tesseract y Ollama para procesamiento real")
    print("  Ver: PROXIMOS_PASOS.md")
    print()


if __name__ == "__main__":
    try:
        ejecutar_prueba()
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

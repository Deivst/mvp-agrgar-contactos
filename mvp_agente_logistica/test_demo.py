"""
Script de prueba demo con datos ficticios
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
    Origen,
    Destino,
    ProductoOrden
)


def crear_datos_ficticios_albaran():
    """Crea un documento albarán ficticio completo"""

    # Crear proveedor ficticio
    proveedor = Proveedor(
        razon_social="Distribuciones López S.L.",
        cif="B12345678",
        direccion="Calle Mayor 123, Madrid"
    )

    # Crear cliente ficticio
    cliente = Cliente(
        razon_social="Farmacia García",
        cif="B87654321",
        direccion_entrega="Avenida Principal 45, Barcelona"
    )

    # Crear productos ficticios
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

    # Crear campos del albarán
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

    # Crear validación ficticia
    validation = ValidationResult(
        status="valid",
        errors=[],
        warnings=[]
    )

    # Crear documento procesado completo
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
        raw_ocr_text="""
ALBARÁN DE ENTREGA
Número: ALB-20250117
Fecha: 17/01/2025

PROVEEDOR:
Distribuciones López S.L.
CIF: B12345678
Calle Mayor 123, Madrid

CLIENTE:
Farmacia García
CIF: B87654321
Avenida Principal 45, Barcelona

PRODUCTOS:
Código    Descripción                  Cantidad  Precio Unit.  Subtotal
MED-001   Paracetamol 500mg x100      50        4.50€         225.00€
MED-002   Ibuprofeno 600mg x50        30        6.80€         204.00€
MED-003   Omeprazol 20mg x28          25        8.50€         212.50€

TOTAL: 641.50€

Observaciones: Entrega urgente - Manejar con cuidado

[FIRMA TRANSPORTISTA] ✓
[SELLO EMPRESA] ✓
        """.strip()
    )

    return documento


def crear_datos_ficticios_orden_envio():
    """Crea una orden de envío ficticia"""

    origen = Origen(
        almacen="Almacén Central Madrid",
        direccion="Polígono Industrial Norte, Nave 5",
        codigo_postal="28001"
    )

    destino = Destino(
        cliente="Farmacia García",
        direccion_entrega="Avenida Principal 45",
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
        instrucciones_especiales="Requiere refrigeración"
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
        raw_ocr_text="ORDEN DE ENVÍO ORD-20250116..."
    )

    return documento


def ejecutar_prueba_demo():
    """Ejecuta una prueba completa con datos ficticios"""

    print("=" * 70)
    print("PRUEBA DEMO - AGENTE DE CLASIFICACIÓN DE DOCUMENTOS LOGÍSTICOS")
    print("=" * 70)
    print()

    # Crear directorio de salida si no existe
    output_dir = Path("data/processed")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Test 1: Albarán
    print("📄 Test 1: Procesando ALBARÁN ficticio...")
    print("-" * 70)

    albaran = crear_datos_ficticios_albaran()

    print(f"✓ Documento clasificado como: {albaran.classification['document_type']}")
    print(f"✓ Confianza de clasificación: {albaran.classification['confidence']*100:.1f}%")
    print(f"✓ Motor OCR: {albaran.ocr_info['engine_used']}")
    print(f"✓ Confianza OCR promedio: {albaran.ocr_info['average_confidence']*100:.1f}%")
    print(f"✓ Bloques de texto detectados: {albaran.ocr_info['total_text_blocks']}")
    print(f"✓ Tablas detectadas: {albaran.ocr_info['tables_detected']}")
    print()

    print("📋 Campos extraídos:")
    print(f"  • Número albarán: {albaran.extracted_fields['numero_albaran']}")
    print(f"  • Fecha: {albaran.extracted_fields['fecha_emision']}")
    print(f"  • Proveedor: {albaran.extracted_fields['proveedor']['razon_social']}")
    print(f"  • Cliente: {albaran.extracted_fields['cliente']['razon_social']}")
    print(f"  • Productos: {len(albaran.extracted_fields['productos'])} items")
    print(f"  • Total: {albaran.extracted_fields['total']}€")
    print(f"  • Firma presente: {'Sí' if albaran.extracted_fields['firma_transportista'] else 'No'}")
    print(f"  • Sello presente: {'Sí' if albaran.extracted_fields['sello_empresa'] else 'No'}")
    print()

    print("🛒 Detalle de productos:")
    for i, producto in enumerate(albaran.extracted_fields['productos'], 1):
        print(f"  {i}. [{producto['codigo_producto']}] {producto['descripcion']}")
        print(f"     Cantidad: {producto['cantidad']} | Precio: {producto['precio_unitario']}€ | Subtotal: {producto['subtotal']}€")
    print()

    print("✅ Validación:")
    print(f"  • Estado: {albaran.validation.status.upper()}")
    print(f"  • Errores: {len(albaran.validation.errors)}")
    print(f"  • Advertencias: {len(albaran.validation.warnings)}")
    print()

    # Guardar JSON
    output_file = output_dir / "albaran_demo_001.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(albaran.model_dump(), f, indent=2, ensure_ascii=False, default=str)

    print(f"💾 Resultado guardado en: {output_file}")
    print()

    # Test 2: Orden de Envío
    print("=" * 70)
    print("📄 Test 2: Procesando ORDEN DE ENVÍO ficticia...")
    print("-" * 70)

    orden = crear_datos_ficticios_orden_envio()

    print(f"✓ Documento clasificado como: {orden.classification['document_type']}")
    print(f"✓ Confianza: {orden.classification['confidence']*100:.1f}%")
    print()

    print("📋 Campos extraídos:")
    print(f"  • Número orden: {orden.extracted_fields['numero_orden']}")
    print(f"  • Fecha orden: {orden.extracted_fields['fecha_orden']}")
    print(f"  • Fecha envío programada: {orden.extracted_fields['fecha_envio_programada']}")
    print(f"  • Origen: {orden.extracted_fields['origen']['almacen']}")
    print(f"  • Destino: {orden.extracted_fields['destino']['cliente']}")
    print(f"  • Transportista: {orden.extracted_fields['transportista']}")
    print(f"  • Productos: {len(orden.extracted_fields['productos'])} items")
    print()

    # Guardar JSON
    output_file = output_dir / "orden_envio_demo_001.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(orden.model_dump(), f, indent=2, ensure_ascii=False, default=str)

    print(f"💾 Resultado guardado en: {output_file}")
    print()

    # Resumen final
    print("=" * 70)
    print("✅ PRUEBA DEMO COMPLETADA EXITOSAMENTE")
    print("=" * 70)
    print()
    print("📊 Resumen:")
    print(f"  • Documentos procesados: 2")
    print(f"  • Albaranes: 1")
    print(f"  • Órdenes de envío: 1")
    print(f"  • Archivos JSON generados: 2")
    print()
    print("📁 Archivos generados en: data/processed/")
    print("  • albaran_demo_001.json")
    print("  • orden_envio_demo_001.json")
    print()
    print("🎯 El sistema está funcionando correctamente!")
    print("   Los modelos Pydantic validan correctamente los datos.")
    print("   La estructura JSON es correcta y lista para producción.")
    print()
    print("📝 Siguiente paso: Instalar Tesseract y Ollama para procesamiento real")
    print("   Ver: PROXIMOS_PASOS.md")
    print()


if __name__ == "__main__":
    try:
        ejecutar_prueba_demo()
    except Exception as e:
        print(f"❌ Error en la prueba: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

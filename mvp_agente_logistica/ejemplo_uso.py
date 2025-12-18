"""
Script de ejemplo para usar el Agente Logistica MVP

Este script muestra como usar el pipeline programaticamente
en lugar de usar la CLI.
"""

from pathlib import Path

from src.core.config import load_config
from src.core.logger import setup_logger
from src.core.pipeline import DocumentProcessingPipeline


def main():
    """Ejemplo de uso programatico del pipeline"""

    print("=" * 60)
    print("EJEMPLO DE USO DEL AGENTE LOGISTICA MVP")
    print("=" * 60)

    # 1. Cargar configuracion
    print("\n[1/4] Cargando configuracion...")
    config = load_config()
    print(f"   - Modelo LLM: {config.llm.model}")
    print(f"   - Motor OCR: {config.ocr.primary_engine}")

    # 2. Configurar logger
    print("\n[2/4] Configurando logger...")
    logger = setup_logger(
        log_level="INFO",
        log_file=config.general.log_file
    )
    logger.info("Sistema iniciado")

    # 3. Crear pipeline
    print("\n[3/4] Inicializando pipeline...")
    pipeline = DocumentProcessingPipeline(config)
    print("   - Pipeline inicializado correctamente")

    # 4. Ejemplo de procesamiento
    print("\n[4/4] Ejemplo de procesamiento:")
    print("\nPara procesar un documento:")
    print("   from src.core.pipeline import DocumentProcessingPipeline")
    print("   pipeline = DocumentProcessingPipeline()")
    print('   result = pipeline.process_document("ruta/al/documento.pdf")')
    print("")
    print("El resultado contendra:")
    print("   - result.document_type: Tipo de documento clasificado")
    print("   - result.extracted_fields: Campos extraidos")
    print("   - result.ocr_average_confidence: Confianza del OCR")
    print("   - result.classification_confidence: Confianza de clasificacion")

    # Ejemplo con archivo de prueba (si existe)
    test_file = "data/test/ejemplo_albaran.pdf"
    if Path(test_file).exists():
        print(f"\n\nProcesando archivo de prueba: {test_file}")
        result = pipeline.process_document(
            file_path=test_file,
            output_path="data/processed/ejemplo_resultado.json"
        )
        print(f"\nResultado:")
        print(f"   Tipo: {result.document_type.value}")
        print(f"   Confianza: {result.classification_confidence:.2%}")
        print(f"   Campos extraidos: {len(result.extracted_fields)}")
    else:
        print(f"\n\nNota: Coloca un documento de prueba en {test_file}")
        print("para ver el procesamiento en accion")

    print("\n" + "=" * 60)
    print("USO POR CLI:")
    print("python src/main.py process --file documento.pdf --output resultado.json")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nProceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n\nError: {e}")
        import traceback
        traceback.print_exc()

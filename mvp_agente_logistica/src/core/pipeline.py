"""
Pipeline principal de procesamiento de documentos
"""
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from ..core.config import Config
from ..core.logger import get_logger
from ..input.loader import DocumentLoader
from ..input.preprocessor import ImagePreprocessor
from ..input.validator import InputValidator
from ..llm.classifier import DocumentClassifier
from ..llm.extractor import FieldExtractor
from ..llm.ollama_client import OllamaClient
from ..models.document import OCRResult, ProcessedDocument
from ..ocr.paddle_engine import PaddleOCREngine
from ..ocr.tesseract_engine import TesseractEngine


class DocumentProcessingPipeline:
    """Pipeline principal de procesamiento"""

    def __init__(self, config: Optional[Config] = None):
        """
        Inicializa el pipeline

        Args:
            config: Configuracion del sistema
        """
        if config is None:
            from ..core.config import load_config
            config = load_config()

        self.config = config
        self.logger = get_logger(__name__)

        # Inicializar componentes
        self.logger.info("Inicializando pipeline de procesamiento...")

        self.loader = DocumentLoader(config)
        self.preprocessor = ImagePreprocessor(config)
        self.validator = InputValidator(config)

        # OCR
        try:
            self.ocr_engine = PaddleOCREngine(config)
            self.ocr_fallback = TesseractEngine(config)
            self.ocr_primary = "PaddleOCR"
        except Exception as e:
            self.logger.warning(f"No se pudo inicializar PaddleOCR: {e}. Usando Tesseract como principal")
            self.ocr_engine = TesseractEngine(config)
            self.ocr_fallback = None
            self.ocr_primary = "Tesseract"

        # LLM
        self.llm_client = OllamaClient(config)
        self.classifier = DocumentClassifier(self.llm_client, config)
        self.extractor = FieldExtractor(self.llm_client, config)

        self.logger.info("Pipeline inicializado correctamente")

    def process_document(self, file_path: str, output_path: Optional[str] = None) -> ProcessedDocument:
        """
        Procesa un documento completo end-to-end

        Args:
            file_path: Ruta al documento
            output_path: Ruta donde guardar el resultado (opcional)

        Returns:
            ProcessedDocument con todos los datos extraidos

        Raises:
            Exception: Si hay error durante el procesamiento
        """
        start_time = time.time()
        self.logger.info(f"============================================")
        self.logger.info(f"Procesando documento: {file_path}")
        self.logger.info(f"============================================")

        try:
            # 1. Validar archivo
            self.logger.info("[1/7] Validando documento...")
            self.validator.validate_document(file_path)

            # 2. Cargar documento
            self.logger.info("[2/7] Cargando documento...")
            images = self.loader.load_document(file_path)
            # Para MVP, procesamos solo la primera pagina
            image = images[0]

            # Validar calidad de imagen
            self.validator.validate_image_quality(image)

            # 3. Preprocesar imagen
            self.logger.info("[3/7] Preprocesando imagen...")
            processed_image = self.preprocessor.preprocess_pipeline(image)

            # 4. Ejecutar OCR
            self.logger.info("[4/7] Ejecutando OCR...")
            ocr_results, ocr_engine_used = self._execute_ocr(processed_image)

            if not ocr_results:
                raise ValueError("No se pudo extraer texto del documento")

            # Concatenar texto OCR
            ocr_text = " ".join([r.text for r in ocr_results])
            self.logger.info(f"OCR extrajo {len(ocr_results)} bloques de texto ({len(ocr_text)} caracteres)")

            # Calcular confianza promedio OCR
            avg_confidence = sum(r.confidence for r in ocr_results) / len(ocr_results)

            # 5. Clasificar documento
            self.logger.info("[5/7] Clasificando documento...")
            doc_type, classification_confidence = self.classifier.classify(ocr_text)

            # 6. Extraer campos
            self.logger.info("[6/7] Extrayendo campos estructurados...")
            extracted_fields = self.extractor.extract_fields(ocr_text, doc_type)

            # 7. Crear documento procesado
            self.logger.info("[7/7] Generando resultado...")

            # Obtener metadata del archivo
            file_path_obj = Path(file_path)
            file_size_kb = file_path_obj.stat().st_size / 1024

            processing_time = time.time() - start_time

            processed_doc = ProcessedDocument(
                file_path=str(file_path),
                file_name=file_path_obj.name,
                file_size_kb=round(file_size_kb, 2),
                processing_timestamp=datetime.now(),
                processing_time_seconds=round(processing_time, 2),
                agent_version=self.config.general.version,
                document_type=doc_type,
                classification_confidence=classification_confidence,
                ocr_engine_used=ocr_engine_used,
                ocr_average_confidence=avg_confidence,
                total_text_blocks=len(ocr_results),
                tables_detected=0,  # TODO: Implementar deteccion de tablas
                signatures_detected=extracted_fields.get('firma_transportista', False) or extracted_fields.get('firma_receptor', False) or extracted_fields.get('firma_origen', False),
                stamps_detected=extracted_fields.get('sello_empresa', False),
                extracted_fields=extracted_fields,
                validation_status="valid",  # TODO: Implementar validacion
                validation_errors=[],
                validation_warnings=[],
                raw_ocr_text=ocr_text if self.config.output.include_raw_ocr else None
            )

            self.logger.info("============================================")
            self.logger.info(f"DOCUMENTO PROCESADO EXITOSAMENTE")
            self.logger.info(f"Tipo: {doc_type.value}")
            self.logger.info(f"Confianza OCR: {avg_confidence:.2%}")
            self.logger.info(f"Confianza Clasificacion: {classification_confidence:.2%}")
            self.logger.info(f"Tiempo total: {processing_time:.2f}s")
            self.logger.info("============================================")

            # Guardar resultado si se especifica output_path
            if output_path:
                self._save_result(processed_doc, output_path)

            return processed_doc

        except Exception as e:
            processing_time = time.time() - start_time
            self.logger.error(f"============================================")
            self.logger.error(f"ERROR AL PROCESAR DOCUMENTO")
            self.logger.error(f"Archivo: {file_path}")
            self.logger.error(f"Error: {e}")
            self.logger.error(f"Tiempo transcurrido: {processing_time:.2f}s")
            self.logger.error("============================================")
            raise

    def _execute_ocr(self, image) -> tuple[List[OCRResult], str]:
        """
        Ejecuta OCR con motor principal y fallback si falla

        Args:
            image: Imagen preprocesada

        Returns:
            Tupla (resultados OCR, nombre del motor usado)
        """
        try:
            results = self.ocr_engine.extract_text(image)
            return results, self.ocr_primary
        except Exception as e:
            self.logger.warning(f"{self.ocr_primary} fallo: {e}")

            if self.ocr_fallback:
                self.logger.info(f"Intentando con motor de fallback...")
                try:
                    results = self.ocr_fallback.extract_text(image)
                    fallback_name = "Tesseract" if self.ocr_primary == "PaddleOCR" else "PaddleOCR"
                    return results, fallback_name
                except Exception as e2:
                    self.logger.error(f"Fallback tambien fallo: {e2}")
                    raise RuntimeError(f"Ambos motores OCR fallaron")
            else:
                raise RuntimeError(f"OCR fallo y no hay fallback disponible")

    def _save_result(self, doc: ProcessedDocument, output_path: str) -> None:
        """Guarda resultado en JSON"""
        import json

        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(
                doc.model_dump(mode='json'),
                f,
                indent=2 if self.config.output.pretty_print else None,
                ensure_ascii=False
            )

        self.logger.info(f"Resultado guardado en: {output_path}")

    def process_batch(self, file_paths: List[str], output_dir: Optional[str] = None) -> List[ProcessedDocument]:
        """
        Procesa un lote de documentos

        Args:
            file_paths: Lista de rutas a documentos
            output_dir: Directorio donde guardar resultados (opcional)

        Returns:
            Lista de documentos procesados
        """
        self.logger.info(f"Procesando lote de {len(file_paths)} documentos...")

        results = []
        for i, file_path in enumerate(file_paths, 1):
            self.logger.info(f"\n--- Procesando documento {i}/{len(file_paths)} ---")

            try:
                # Generar output path si se especifica directorio
                output_path = None
                if output_dir:
                    filename = Path(file_path).stem + ".json"
                    output_path = str(Path(output_dir) / filename)

                result = self.process_document(file_path, output_path)
                results.append(result)

            except Exception as e:
                self.logger.error(f"Error procesando {file_path}: {e}")
                continue

        self.logger.info(f"\nLote completado: {len(results)}/{len(file_paths)} documentos procesados")
        return results

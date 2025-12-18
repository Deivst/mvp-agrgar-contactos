"""
Clasificador de documentos usando LLM
"""
from typing import Optional, Tuple

from ..core.config import Config
from ..core.logger import get_logger
from ..models.document import DocumentType
from .ollama_client import OllamaClient
from .prompts import CLASSIFICATION_PROMPT, CLASSIFICATION_SYSTEM_PROMPT


class DocumentClassifier:
    """Clasifica tipo de documento"""

    def __init__(self, llm_client: Optional[OllamaClient] = None, config: Optional[Config] = None):
        """
        Inicializa el clasificador

        Args:
            llm_client: Cliente LLM (crea uno nuevo si es None)
            config: Configuracion del sistema
        """
        self.config = config
        self.logger = get_logger(__name__)

        if llm_client is None:
            self.llm = OllamaClient(config)
        else:
            self.llm = llm_client

        if config:
            self.confidence_threshold = config.llm.classification.confidence_threshold
        else:
            self.confidence_threshold = 0.8

    def classify(self, ocr_text: str) -> Tuple[DocumentType, float]:
        """
        Clasifica documento en una de las categorias

        Args:
            ocr_text: Texto extraido por OCR

        Returns:
            Tupla (DocumentType, confidence)

        Raises:
            ValueError: Si no se puede clasificar el documento
        """
        self.logger.info("Clasificando documento...")

        # Truncar texto si es muy largo (para evitar timeouts)
        max_length = 2000
        if len(ocr_text) > max_length:
            ocr_text_truncated = ocr_text[:max_length] + "..."
            self.logger.debug(f"Texto OCR truncado a {max_length} caracteres")
        else:
            ocr_text_truncated = ocr_text

        # Generar prompt
        prompt = CLASSIFICATION_PROMPT.format(ocr_text=ocr_text_truncated)

        try:
            # Llamar al LLM
            response = self.llm.generate_json(
                prompt=prompt,
                system=CLASSIFICATION_SYSTEM_PROMPT
            )

            # Extraer resultado
            doc_type_str = response.get('document_type', '').upper()
            confidence = float(response.get('confidence', 0.0))
            reasoning = response.get('reasoning', '')

            self.logger.debug(f"Razonamiento: {reasoning}")

            # Validar tipo de documento
            try:
                doc_type = DocumentType(doc_type_str)
            except ValueError:
                raise ValueError(f"Tipo de documento invalido: {doc_type_str}")

            # Verificar confianza
            if confidence < self.confidence_threshold:
                self.logger.warning(
                    f"Confianza de clasificacion baja: {confidence:.2f} "
                    f"(umbral: {self.confidence_threshold})"
                )

            self.logger.info(
                f"Documento clasificado como: {doc_type.value} "
                f"(confianza: {confidence:.2f})"
            )

            return doc_type, confidence

        except Exception as e:
            self.logger.error(f"Error durante clasificacion: {e}")
            raise ValueError(f"No se pudo clasificar el documento: {e}")

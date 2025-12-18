"""
Motor OCR basado en Tesseract (fallback)
"""
from typing import List, Optional

import cv2
import numpy as np
import pytesseract

from ..core.config import Config
from ..core.logger import get_logger
from ..models.document import BBox, OCRResult


class TesseractEngine:
    """Motor de respaldo usando Tesseract"""

    def __init__(self, config: Optional[Config] = None):
        """
        Inicializa el motor Tesseract

        Args:
            config: Configuracion del sistema
        """
        self.config = config
        self.logger = get_logger(__name__)

        # Configuracion OCR
        if config:
            self.language = config.ocr.language
            self.confidence_threshold = config.ocr.confidence_threshold
            tesseract_config = config.ocr.tesseract
            self.psm = tesseract_config.psm if tesseract_config else 3
            self.oem = tesseract_config.oem if tesseract_config else 3
        else:
            self.language = "spa"  # Tesseract usa 'spa' para español
            self.confidence_threshold = 0.7
            self.psm = 3
            self.oem = 3

        # Verificar que Tesseract esta instalado
        try:
            pytesseract.get_tesseract_version()
            self.logger.info("Tesseract detectado correctamente")
        except Exception as e:
            self.logger.error(f"Tesseract no esta instalado o no es accesible: {e}")
            raise RuntimeError(f"Tesseract no disponible: {e}")

    def extract_text(
        self,
        image: np.ndarray,
        confidence_threshold: Optional[float] = None
    ) -> List[OCRResult]:
        """
        Extrae texto con Tesseract

        Args:
            image: Imagen en formato numpy array (BGR)
            confidence_threshold: Umbral de confianza (usa config si None)

        Returns:
            Lista de OCRResult con texto, bbox y confianza

        Raises:
            ValueError: Si la imagen es invalida
            RuntimeError: Si el OCR falla
        """
        if image is None or image.size == 0:
            raise ValueError("Imagen invalida para OCR")

        if confidence_threshold is None:
            confidence_threshold = self.confidence_threshold

        self.logger.info("Ejecutando Tesseract...")

        try:
            # Configurar Tesseract
            custom_config = f'--oem {self.oem} --psm {self.psm}'

            # Ejecutar OCR con datos detallados
            data = pytesseract.image_to_data(
                image,
                lang=self.language,
                config=custom_config,
                output_type=pytesseract.Output.DICT
            )

            # Procesar resultados
            ocr_results = []
            n_boxes = len(data['text'])

            for i in range(n_boxes):
                # Obtener confianza (Tesseract usa -1 para bloques vacios)
                conf = float(data['conf'][i])
                if conf < 0:
                    continue

                # Normalizar confianza (Tesseract da 0-100, convertir a 0-1)
                confidence = conf / 100.0

                # Filtrar por confianza
                if confidence < confidence_threshold:
                    continue

                # Obtener texto
                text = data['text'][i].strip()
                if not text:
                    continue

                # Crear BBox
                x = data['left'][i]
                y = data['top'][i]
                w = data['width'][i]
                h = data['height'][i]

                bbox = BBox(
                    x1=int(x),
                    y1=int(y),
                    x2=int(x + w),
                    y2=int(y + h)
                )

                # Crear OCRResult
                ocr_result = OCRResult(
                    text=text,
                    bbox=bbox,
                    confidence=confidence
                )
                ocr_results.append(ocr_result)

            self.logger.info(f"Tesseract extrajo {len(ocr_results)} bloques de texto")
            return ocr_results

        except Exception as e:
            self.logger.error(f"Error durante OCR con Tesseract: {e}")
            raise RuntimeError(f"Error durante OCR con Tesseract: {e}")

    def extract_text_simple(self, image: np.ndarray) -> str:
        """
        Extrae texto simple sin coordenadas

        Args:
            image: Imagen en formato numpy array (BGR)

        Returns:
            Texto extraido

        Raises:
            RuntimeError: Si el OCR falla
        """
        try:
            custom_config = f'--oem {self.oem} --psm {self.psm}'
            text = pytesseract.image_to_string(
                image,
                lang=self.language,
                config=custom_config
            )
            return text.strip()

        except Exception as e:
            self.logger.error(f"Error durante OCR simple con Tesseract: {e}")
            raise RuntimeError(f"Error durante OCR simple con Tesseract: {e}")

    def get_average_confidence(self, results: List[OCRResult]) -> float:
        """
        Calcula confianza promedio de resultados OCR

        Args:
            results: Lista de resultados OCR

        Returns:
            Confianza promedio (0-1)
        """
        if not results:
            return 0.0

        total_confidence = sum(r.confidence for r in results)
        return total_confidence / len(results)

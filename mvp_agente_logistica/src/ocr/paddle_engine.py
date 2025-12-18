"""
Motor OCR basado en PaddleOCR
"""
from typing import List, Optional

import cv2
import numpy as np
import pandas as pd

from ..core.config import Config
from ..core.logger import get_logger
from ..models.document import BBox, OCRResult


class PaddleOCREngine:
    """Motor principal de OCR usando PaddleOCR"""

    def __init__(self, config: Optional[Config] = None):
        """
        Inicializa el motor PaddleOCR

        Args:
            config: Configuracion del sistema
        """
        self.config = config
        self.logger = get_logger(__name__)

        # Configuracion OCR
        if config:
            self.language = config.ocr.language
            self.use_gpu = config.ocr.use_gpu
            self.confidence_threshold = config.ocr.confidence_threshold
            paddle_config = config.ocr.paddleocr
        else:
            self.language = "es"
            self.use_gpu = False
            self.confidence_threshold = 0.7
            paddle_config = None

        # Inicializar PaddleOCR
        try:
            from paddleocr import PaddleOCR

            self.ocr = PaddleOCR(
                use_angle_cls=paddle_config.use_angle_cls if paddle_config else True,
                lang=self.language,
                use_gpu=self.use_gpu,
                show_log=False,
                det_db_thresh=paddle_config.det_db_thresh if paddle_config else 0.3,
                det_db_box_thresh=paddle_config.det_db_box_thresh if paddle_config else 0.6,
                det_db_unclip_ratio=paddle_config.det_db_unclip_ratio if paddle_config else 1.5
            )
            self.logger.info("PaddleOCR inicializado correctamente")

        except Exception as e:
            self.logger.error(f"Error al inicializar PaddleOCR: {e}")
            raise RuntimeError(f"No se pudo inicializar PaddleOCR: {e}")

    def extract_text(
        self,
        image: np.ndarray,
        confidence_threshold: Optional[float] = None
    ) -> List[OCRResult]:
        """
        Extrae texto completo de la imagen

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

        self.logger.info("Ejecutando PaddleOCR...")

        try:
            # Ejecutar OCR
            result = self.ocr.ocr(image, cls=True)

            if not result or not result[0]:
                self.logger.warning("PaddleOCR no detecto texto en la imagen")
                return []

            # Procesar resultados
            ocr_results = []
            for line in result[0]:
                bbox_coords = line[0]  # [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
                text_info = line[1]    # (text, confidence)
                text = text_info[0]
                confidence = text_info[1]

                # Filtrar por confianza
                if confidence < confidence_threshold:
                    self.logger.debug(
                        f"Texto descartado por baja confianza ({confidence:.2f}): {text}"
                    )
                    continue

                # Crear BBox
                x_coords = [point[0] for point in bbox_coords]
                y_coords = [point[1] for point in bbox_coords]

                bbox = BBox(
                    x1=int(min(x_coords)),
                    y1=int(min(y_coords)),
                    x2=int(max(x_coords)),
                    y2=int(max(y_coords))
                )

                # Crear OCRResult
                ocr_result = OCRResult(
                    text=text,
                    bbox=bbox,
                    confidence=confidence
                )
                ocr_results.append(ocr_result)

            self.logger.info(f"PaddleOCR extrajo {len(ocr_results)} bloques de texto")
            return ocr_results

        except Exception as e:
            self.logger.error(f"Error durante OCR: {e}")
            raise RuntimeError(f"Error durante OCR: {e}")

    def extract_region(self, image: np.ndarray, bbox: BBox) -> str:
        """
        Extrae texto de una region especifica

        Args:
            image: Imagen completa
            bbox: Bounding box de la region

        Returns:
            Texto extraido de la region
        """
        # Recortar region
        region = image[bbox.y1:bbox.y2, bbox.x1:bbox.x2]

        # Ejecutar OCR en region
        results = self.extract_text(region)

        # Concatenar texto
        text = " ".join([r.text for r in results])

        return text

    def extract_table(
        self,
        image: np.ndarray,
        table_bbox: Optional[BBox] = None
    ) -> pd.DataFrame:
        """
        Extrae tabla como DataFrame

        Args:
            image: Imagen del documento
            table_bbox: Bounding box de la tabla (opcional)

        Returns:
            DataFrame con los datos de la tabla

        Note:
            Implementacion basica. Para tablas complejas se recomienda
            usar PaddleOCR-Table o metodos especializados
        """
        # Si se proporciona bbox, recortar region
        if table_bbox:
            table_image = image[table_bbox.y1:table_bbox.y2, table_bbox.x1:table_bbox.x2]
        else:
            table_image = image

        # Extraer texto de la tabla
        ocr_results = self.extract_text(table_image)

        # Ordenar resultados por posicion vertical (y1)
        sorted_results = sorted(ocr_results, key=lambda r: r.bbox.y1)

        # Agrupar por filas (usando tolerancia vertical)
        rows = []
        current_row = []
        current_y = None
        y_tolerance = 10

        for result in sorted_results:
            if current_y is None:
                current_y = result.bbox.y1
                current_row.append(result)
            elif abs(result.bbox.y1 - current_y) <= y_tolerance:
                current_row.append(result)
            else:
                # Nueva fila
                # Ordenar elementos de la fila por x1
                current_row_sorted = sorted(current_row, key=lambda r: r.bbox.x1)
                rows.append([r.text for r in current_row_sorted])
                current_row = [result]
                current_y = result.bbox.y1

        # Agregar ultima fila
        if current_row:
            current_row_sorted = sorted(current_row, key=lambda r: r.bbox.x1)
            rows.append([r.text for r in current_row_sorted])

        # Crear DataFrame
        if rows:
            # Usar primera fila como headers si tiene sentido
            max_cols = max(len(row) for row in rows)

            # Normalizar numero de columnas
            normalized_rows = []
            for row in rows:
                while len(row) < max_cols:
                    row.append("")
                normalized_rows.append(row[:max_cols])

            df = pd.DataFrame(normalized_rows[1:], columns=normalized_rows[0] if len(normalized_rows) > 1 else None)
            return df
        else:
            return pd.DataFrame()

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

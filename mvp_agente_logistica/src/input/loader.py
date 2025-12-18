"""
Cargador de documentos desde diferentes fuentes
"""
import os
from pathlib import Path
from typing import List, Optional

import cv2
import numpy as np
from pdf2image import convert_from_path
from PIL import Image

from ..core.config import Config
from ..core.logger import get_logger


class DocumentLoader:
    """Carga documentos desde diferentes fuentes"""

    def __init__(self, config: Optional[Config] = None):
        """
        Inicializa el cargador

        Args:
            config: Configuracion del sistema
        """
        self.config = config
        self.logger = get_logger(__name__)

        # Formatos soportados
        self.image_formats = ['jpg', 'jpeg', 'png', 'tiff', 'tif', 'bmp']
        self.pdf_formats = ['pdf']

        if config:
            self.max_file_size_mb = config.input.max_file_size_mb
            self.min_resolution_dpi = config.input.min_resolution_dpi
        else:
            self.max_file_size_mb = 20
            self.min_resolution_dpi = 150

    def load_image(self, path: str) -> np.ndarray:
        """
        Carga imagen desde archivo

        Args:
            path: Ruta al archivo de imagen

        Returns:
            Imagen en formato numpy array (BGR)

        Raises:
            FileNotFoundError: Si el archivo no existe
            ValueError: Si el formato no es soportado o el archivo es invalido
        """
        self.logger.info(f"Cargando imagen: {path}")

        # Verificar que el archivo existe
        if not Path(path).exists():
            raise FileNotFoundError(f"Archivo no encontrado: {path}")

        # Verificar extension
        extension = Path(path).suffix.lower().lstrip('.')
        if extension not in self.image_formats:
            raise ValueError(f"Formato de imagen no soportado: {extension}")

        # Verificar tamano
        file_size_mb = Path(path).stat().st_size / (1024 * 1024)
        if file_size_mb > self.max_file_size_mb:
            raise ValueError(
                f"Archivo demasiado grande ({file_size_mb:.2f} MB). "
                f"Maximo permitido: {self.max_file_size_mb} MB"
            )

        # Cargar imagen
        try:
            image = cv2.imread(path)
            if image is None:
                raise ValueError(f"No se pudo cargar la imagen: {path}")

            self.logger.info(f"Imagen cargada: {image.shape[1]}x{image.shape[0]} pixels")
            return image

        except Exception as e:
            self.logger.error(f"Error al cargar imagen: {e}")
            raise ValueError(f"Error al cargar imagen: {e}")

    def load_pdf(self, path: str, dpi: Optional[int] = None) -> List[np.ndarray]:
        """
        Carga PDF y convierte a lista de imagenes

        Args:
            path: Ruta al archivo PDF
            dpi: DPI para conversion (usa min_resolution_dpi si None)

        Returns:
            Lista de imagenes (una por pagina) en formato numpy array (BGR)

        Raises:
            FileNotFoundError: Si el archivo no existe
            ValueError: Si el formato no es soportado o el archivo es invalido
        """
        self.logger.info(f"Cargando PDF: {path}")

        # Verificar que el archivo existe
        if not Path(path).exists():
            raise FileNotFoundError(f"Archivo no encontrado: {path}")

        # Verificar extension
        extension = Path(path).suffix.lower().lstrip('.')
        if extension not in self.pdf_formats:
            raise ValueError(f"Formato no es PDF: {extension}")

        # Verificar tamano
        file_size_mb = Path(path).stat().st_size / (1024 * 1024)
        if file_size_mb > self.max_file_size_mb:
            raise ValueError(
                f"Archivo demasiado grande ({file_size_mb:.2f} MB). "
                f"Maximo permitido: {self.max_file_size_mb} MB"
            )

        # Convertir PDF a imagenes
        try:
            if dpi is None:
                dpi = self.min_resolution_dpi

            self.logger.info(f"Convirtiendo PDF a imagenes (DPI: {dpi})...")
            pil_images = convert_from_path(path, dpi=dpi)

            # Convertir de PIL a numpy array (BGR)
            images = []
            for i, pil_image in enumerate(pil_images):
                # Convertir PIL (RGB) a numpy array (BGR)
                image_rgb = np.array(pil_image)
                image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
                images.append(image_bgr)
                self.logger.info(f"Pagina {i+1}: {image_bgr.shape[1]}x{image_bgr.shape[0]} pixels")

            self.logger.info(f"PDF convertido: {len(images)} paginas")
            return images

        except Exception as e:
            self.logger.error(f"Error al cargar PDF: {e}")
            raise ValueError(f"Error al cargar PDF: {e}")

    def load_document(self, path: str) -> List[np.ndarray]:
        """
        Carga documento (imagen o PDF) y retorna lista de imagenes

        Args:
            path: Ruta al archivo

        Returns:
            Lista de imagenes en formato numpy array (BGR)

        Raises:
            FileNotFoundError: Si el archivo no existe
            ValueError: Si el formato no es soportado
        """
        extension = Path(path).suffix.lower().lstrip('.')

        if extension in self.image_formats:
            # Retornar imagen como lista de un elemento
            return [self.load_image(path)]
        elif extension in self.pdf_formats:
            # Retornar lista de imagenes del PDF
            return self.load_pdf(path)
        else:
            raise ValueError(f"Formato de archivo no soportado: {extension}")

    def validate_document(self, doc: np.ndarray) -> bool:
        """
        Valida integridad del documento

        Args:
            doc: Imagen a validar

        Returns:
            True si el documento es valido

        Raises:
            ValueError: Si el documento no es valido
        """
        # Verificar que es un array numpy
        if not isinstance(doc, np.ndarray):
            raise ValueError("El documento debe ser un numpy array")

        # Verificar que tiene 3 dimensiones (alto, ancho, canales)
        if len(doc.shape) != 3:
            raise ValueError(f"La imagen debe tener 3 dimensiones, tiene {len(doc.shape)}")

        # Verificar que tiene 3 canales (BGR)
        if doc.shape[2] != 3:
            raise ValueError(f"La imagen debe tener 3 canales, tiene {doc.shape[2]}")

        # Verificar resolucion minima (aproximada)
        height, width = doc.shape[:2]
        if width < 800 or height < 600:
            self.logger.warning(
                f"Resolucion baja ({width}x{height}). "
                "Puede afectar la calidad del OCR"
            )

        # Verificar que no esta vacia
        if np.sum(doc) == 0:
            raise ValueError("La imagen esta vacia (todos los pixels en negro)")

        return True

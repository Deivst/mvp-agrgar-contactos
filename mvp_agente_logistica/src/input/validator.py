"""
Validador de documentos de entrada
"""
from pathlib import Path
from typing import Optional

import numpy as np

from ..core.config import Config
from ..core.logger import get_logger


class InputValidator:
    """Valida documentos de entrada antes de procesarlos"""

    def __init__(self, config: Optional[Config] = None):
        """
        Inicializa el validador

        Args:
            config: Configuracion del sistema
        """
        self.config = config
        self.logger = get_logger(__name__)

        if config:
            self.supported_formats = config.input.supported_formats
            self.max_file_size_mb = config.input.max_file_size_mb
            self.min_resolution_dpi = config.input.min_resolution_dpi
        else:
            self.supported_formats = ['jpg', 'jpeg', 'png', 'tiff', 'pdf']
            self.max_file_size_mb = 20
            self.min_resolution_dpi = 150

    def validate_file_path(self, path: str) -> bool:
        """
        Valida que el archivo existe y es accesible

        Args:
            path: Ruta al archivo

        Returns:
            True si el archivo es valido

        Raises:
            FileNotFoundError: Si el archivo no existe
            PermissionError: Si no hay permisos de lectura
        """
        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(f"El archivo no existe: {path}")

        if not file_path.is_file():
            raise ValueError(f"La ruta no es un archivo: {path}")

        if not os.access(path, os.R_OK):
            raise PermissionError(f"No hay permisos de lectura: {path}")

        return True

    def validate_file_format(self, path: str) -> bool:
        """
        Valida que el formato del archivo es soportado

        Args:
            path: Ruta al archivo

        Returns:
            True si el formato es soportado

        Raises:
            ValueError: Si el formato no es soportado
        """
        extension = Path(path).suffix.lower().lstrip('.')

        if extension not in self.supported_formats:
            raise ValueError(
                f"Formato '{extension}' no soportado. "
                f"Formatos validos: {', '.join(self.supported_formats)}"
            )

        return True

    def validate_file_size(self, path: str) -> bool:
        """
        Valida que el tamano del archivo no excede el limite

        Args:
            path: Ruta al archivo

        Returns:
            True si el tamano es valido

        Raises:
            ValueError: Si el archivo es demasiado grande
        """
        file_size_bytes = Path(path).stat().st_size
        file_size_mb = file_size_bytes / (1024 * 1024)

        if file_size_mb > self.max_file_size_mb:
            raise ValueError(
                f"Archivo demasiado grande ({file_size_mb:.2f} MB). "
                f"Maximo permitido: {self.max_file_size_mb} MB"
            )

        self.logger.debug(f"Tamano del archivo: {file_size_mb:.2f} MB")
        return True

    def validate_image_quality(self, image: np.ndarray) -> bool:
        """
        Valida la calidad de la imagen (resolucion, claridad)

        Args:
            image: Imagen a validar

        Returns:
            True si la calidad es aceptable

        Raises:
            ValueError: Si la calidad es muy baja
        """
        height, width = image.shape[:2]

        # Validar resolucion minima (aproximada)
        if width < 800 or height < 600:
            self.logger.warning(
                f"Resolucion baja ({width}x{height}). "
                "Puede afectar la calidad del OCR"
            )

        # Validar que la imagen no este completamente en blanco o negro
        mean_value = np.mean(image)
        if mean_value < 10:
            raise ValueError("La imagen esta demasiado oscura (puede estar en negro)")
        if mean_value > 245:
            raise ValueError("La imagen esta demasiado clara (puede estar en blanco)")

        # Validar que tenga suficiente contenido (varianza)
        std_value = np.std(image)
        if std_value < 10:
            self.logger.warning(
                f"La imagen tiene muy poca variacion (std: {std_value:.2f}). "
                "Puede estar vacia o muy homogenea"
            )

        return True

    def validate_document(self, path: str, image: Optional[np.ndarray] = None) -> bool:
        """
        Valida documento completo (archivo + imagen si se proporciona)

        Args:
            path: Ruta al archivo
            image: Imagen cargada (opcional)

        Returns:
            True si el documento es valido

        Raises:
            ValueError: Si el documento no es valido
        """
        self.logger.info(f"Validando documento: {path}")

        # Validar archivo
        self.validate_file_path(path)
        self.validate_file_format(path)
        self.validate_file_size(path)

        # Validar imagen si se proporciona
        if image is not None:
            self.validate_image_quality(image)

        self.logger.info("Documento validado correctamente")
        return True


import os

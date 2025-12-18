"""
Preprocesador de imagenes para mejorar calidad de OCR
"""
from typing import Optional

import cv2
import numpy as np

from ..core.config import Config
from ..core.logger import get_logger


class ImagePreprocessor:
    """Preprocesa imagenes para mejorar OCR"""

    def __init__(self, config: Optional[Config] = None):
        """
        Inicializa el preprocesador

        Args:
            config: Configuracion del sistema
        """
        self.config = config
        self.logger = get_logger(__name__)

        if config:
            self.denoise_enabled = config.preprocessing.denoise
            self.denoise_strength = config.preprocessing.denoise_strength
            self.deskew_enabled = config.preprocessing.deskew
            self.deskew_threshold = config.preprocessing.deskew_threshold
            self.enhance_contrast = config.preprocessing.enhance_contrast
            self.contrast_method = config.preprocessing.contrast_method
            self.binarize_enabled = config.preprocessing.binarize
        else:
            self.denoise_enabled = True
            self.denoise_strength = 3
            self.deskew_enabled = True
            self.deskew_threshold = 0.5
            self.enhance_contrast = True
            self.contrast_method = "clahe"
            self.binarize_enabled = False

    def denoise(self, image: np.ndarray) -> np.ndarray:
        """
        Reduce ruido usando Non-Local Means Denoising

        Args:
            image: Imagen de entrada (BGR o Grayscale)

        Returns:
            Imagen sin ruido

        Raises:
            ValueError: Si la imagen es invalida
        """
        if image is None or image.size == 0:
            raise ValueError("Imagen invalida para denoise")

        self.logger.debug("Aplicando denoise...")

        if len(image.shape) == 3:
            # Imagen a color
            denoised = cv2.fastNlMeansDenoisingColored(
                image,
                None,
                h=self.denoise_strength,
                hColor=self.denoise_strength,
                templateWindowSize=7,
                searchWindowSize=21
            )
        else:
            # Imagen en escala de grises
            denoised = cv2.fastNlMeansDenoising(
                image,
                None,
                h=self.denoise_strength,
                templateWindowSize=7,
                searchWindowSize=21
            )

        return denoised

    def deskew(self, image: np.ndarray) -> np.ndarray:
        """
        Corrige inclinacion de la imagen usando deteccion de lineas

        Args:
            image: Imagen de entrada (BGR o Grayscale)

        Returns:
            Imagen corregida

        Raises:
            ValueError: Si la imagen es invalida
        """
        if image is None or image.size == 0:
            raise ValueError("Imagen invalida para deskew")

        self.logger.debug("Aplicando deskew...")

        # Convertir a escala de grises si es necesario
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        # Detectar bordes
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)

        # Detectar lineas usando transformada de Hough
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

        if lines is None or len(lines) == 0:
            self.logger.debug("No se detectaron lineas para deskew")
            return image

        # Calcular angulos de las lineas
        angles = []
        for line in lines:
            rho, theta = line[0]
            angle = (theta - np.pi / 2) * 180 / np.pi
            # Filtrar angulos extremos
            if abs(angle) < 45:
                angles.append(angle)

        if len(angles) == 0:
            self.logger.debug("No se encontraron angulos validos para deskew")
            return image

        # Calcular angulo mediano
        median_angle = np.median(angles)

        self.logger.debug(f"Angulo de inclinacion detectado: {median_angle:.2f} grados")

        # Rotar si el angulo supera el umbral
        if abs(median_angle) > self.deskew_threshold:
            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, median_angle, 1.0)
            rotated = cv2.warpAffine(
                image, M, (w, h),
                flags=cv2.INTER_CUBIC,
                borderMode=cv2.BORDER_REPLICATE
            )
            self.logger.debug(f"Imagen rotada {median_angle:.2f} grados")
            return rotated
        else:
            self.logger.debug("Angulo de inclinacion dentro del umbral, no se rota")
            return image

    def enhance_contrast_image(self, image: np.ndarray) -> np.ndarray:
        """
        Mejora contraste usando CLAHE o ecualizacion de histograma

        Args:
            image: Imagen de entrada (BGR o Grayscale)

        Returns:
            Imagen con contraste mejorado

        Raises:
            ValueError: Si la imagen es invalida
        """
        if image is None or image.size == 0:
            raise ValueError("Imagen invalida para enhance_contrast")

        self.logger.debug(f"Aplicando enhancement de contraste ({self.contrast_method})...")

        # Convertir a escala de grises si es necesario
        if len(image.shape) == 3:
            # Convertir a LAB para procesar solo el canal de luminosidad
            lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            l, a, b = cv2.split(lab)
            gray_channel = l
            is_color = True
        else:
            gray_channel = image.copy()
            is_color = False

        # Aplicar metodo de enhancement
        if self.contrast_method == "clahe":
            # CLAHE (Contrast Limited Adaptive Histogram Equalization)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced = clahe.apply(gray_channel)
        else:
            # Ecualizacion de histograma simple
            enhanced = cv2.equalizeHist(gray_channel)

        # Reconstruir imagen a color si es necesario
        if is_color:
            lab_enhanced = cv2.merge([enhanced, a, b])
            result = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR)
        else:
            result = enhanced

        return result

    def binarize(self, image: np.ndarray) -> np.ndarray:
        """
        Binarizacion adaptativa usando metodo de Otsu

        Args:
            image: Imagen de entrada (BGR o Grayscale)

        Returns:
            Imagen binarizada (blanco y negro)

        Raises:
            ValueError: Si la imagen es invalida
        """
        if image is None or image.size == 0:
            raise ValueError("Imagen invalida para binarize")

        self.logger.debug("Aplicando binarizacion...")

        # Convertir a escala de grises si es necesario
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image.copy()

        # Aplicar threshold de Otsu
        _, binary = cv2.threshold(
            gray, 0, 255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )

        return binary

    def preprocess_pipeline(self, image: np.ndarray) -> np.ndarray:
        """
        Ejecuta pipeline completo de preprocesamiento segun configuracion

        Args:
            image: Imagen de entrada (BGR)

        Returns:
            Imagen preprocesada

        Raises:
            ValueError: Si la imagen es invalida
        """
        if image is None or image.size == 0:
            raise ValueError("Imagen invalida para preprocessing")

        self.logger.info("Iniciando pipeline de preprocesamiento...")

        processed = image.copy()

        # 1. Denoise
        if self.denoise_enabled:
            processed = self.denoise(processed)

        # 2. Deskew
        if self.deskew_enabled:
            processed = self.deskew(processed)

        # 3. Enhance contrast
        if self.enhance_contrast:
            processed = self.enhance_contrast_image(processed)

        # 4. Binarize (opcional, generalmente mejor no binarizar para OCR moderno)
        if self.binarize_enabled:
            processed = self.binarize(processed)

        self.logger.info("Pipeline de preprocesamiento completado")

        return processed

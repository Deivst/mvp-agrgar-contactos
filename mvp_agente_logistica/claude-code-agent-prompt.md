# Prompt Chain-of-Thought para Agente Claude Code
## Backend - Agente de Clasificación de Documentos Logísticos

---

## 🎯 OBJETIVO DEL AGENTE

Eres un agente especializado de Claude Code encargado de **desarrollar y testear el backend completo** del sistema de clasificación y validación de documentos logísticos descrito en el PRD/SRS.

Tu misión es implementar el MVP funcional siguiendo una metodología estructurada con **Chain-of-Thought (CoT)**, pensando en voz alta sobre cada decisión técnica y validando tu trabajo mediante tests automatizados.

---

## 📚 CONTEXTO DEL PROYECTO

**Sistema:** Agente de IA para clasificación, extracción y validación de campos clave en documentación logística

**Stack Tecnológico:**
- Python 3.10+
- PaddleOCR (OCR principal)
- Tesseract (OCR fallback)
- Ollama + Llama 3 8B (LLM local)
- OpenCV (preprocesamiento)
- Pydantic (validación de datos)
- Typer (CLI)
- pytest (testing)

**Tipos de Documentos:**
1. Albarán de Entrega
2. Orden de Envío
3. Nota de Recepción
4. Parte de Transporte

**Componentes Principales:**
1. Input Handler (carga y preprocesamiento)
2. OCR Engine (PaddleOCR + Tesseract)
3. LLM Engine (clasificación y extracción)
4. Validator Engine (validación individual y cruzada)
5. Output Handler (JSON + reportes)

---

## 🧠 METODOLOGÍA CHAIN-OF-THOUGHT

Para cada tarea que realices, **DEBES seguir este proceso de pensamiento estructurado**:

### Paso 1: ENTENDER
- ¿Qué componente estoy implementando?
- ¿Cuáles son sus responsabilidades exactas?
- ¿Qué entradas recibe y qué salidas debe producir?
- ¿Con qué otros componentes interactúa?

### Paso 2: PLANIFICAR
- ¿Cuál es la mejor estructura de clases/funciones?
- ¿Qué patrones de diseño son apropiados?
- ¿Qué dependencias externas necesito?
- ¿Qué casos edge debo manejar?

### Paso 3: DISEÑAR
- Diseñar firmas de métodos con type hints
- Definir modelos Pydantic necesarios
- Identificar posibles excepciones
- Pensar en testabilidad desde el diseño

### Paso 4: IMPLEMENTAR
- Escribir código limpio y documentado
- Incluir docstrings detallados
- Manejar errores apropiadamente
- Logging en puntos clave

### Paso 5: TESTEAR
- Escribir tests unitarios (pytest)
- Tests de integración cuando aplique
- Casos edge y manejo de errores
- Validar con datos reales

### Paso 6: VALIDAR
- ¿El código cumple los requisitos?
- ¿Los tests pasan?
- ¿La cobertura es adecuada?
- ¿Hay code smells o mejoras posibles?

---

## 📋 PLAN DE IMPLEMENTACIÓN ESTRUCTURADO

Sigue este orden de implementación, completando cada fase antes de avanzar:

### **FASE 1: Setup del Proyecto** ⚙️

**Objetivo:** Preparar estructura base y configuración

**Tareas:**
1. Crear estructura de directorios completa
2. Configurar `pyproject.toml` y `requirements.txt`
3. Configurar `.env` y `config.yaml`
4. Crear módulo de configuración (`src/core/config.py`)
5. Configurar sistema de logging (`src/core/logger.py`)
6. Escribir tests básicos de configuración

**Chain-of-Thought para Tarea 1 (ejemplo):**

```
ENTENDER:
- Necesito crear la estructura de directorios según el SRS
- Debe incluir: src/, data/, tests/, templates/, scripts/, docs/
- Cada directorio src/ debe tener subcarpetas por componente
- Necesito __init__.py en cada paquete Python

PLANIFICAR:
- Crear script que genere toda la estructura automáticamente
- Incluir archivos .gitkeep en directorios vacíos
- Añadir .gitignore apropiado
- Crear README.md básico en cada subdirectorio

DISEÑAR:
Script: scripts/setup_project_structure.py
- Función create_directory_structure()
- Lista de directorios requeridos
- Creación recursiva con manejo de errores

IMPLEMENTAR:
[Escribir el código]

TESTEAR:
- Verificar que todos los directorios se crean
- Verificar que __init__.py está presente
- Validar .gitignore funciona

VALIDAR:
- ✓ Estructura completa creada
- ✓ Tests pasan
- ✓ Sin errores de permisos
```

**Entregables Fase 1:**
- [ ] Estructura de directorios completa
- [ ] Archivos de configuración
- [ ] Sistema de logging funcional
- [ ] Tests de setup pasando

---

### **FASE 2: Modelos de Datos** 📊

**Objetivo:** Implementar todos los modelos Pydantic según el SRS

**Tareas:**
1. Crear modelos base (`src/models/document.py`)
   - `BBox`: Bounding box de región
   - `OCRResult`: Resultado OCR por línea
   - `TableCell`: Celda de tabla

2. Crear modelos de campos (`src/models/fields.py`)
   - `Proveedor`, `Cliente`
   - `Producto`
   - Campos específicos por tipo de documento

3. Crear schemas de documentos (`src/models/schemas.py`)
   - `AlbaranSchema`
   - `OrdenEnvioSchema`
   - `NotaRecepcionSchema`
   - `ParteTransporteSchema`

4. Crear modelos de validación (`src/models/validation.py`)
   - `Discrepancy`
   - `ValidationReport`
   - `ProcessedDocument`

**Chain-of-Thought para Tarea 1:**

```
ENTENDER:
- Necesito modelos que representen datos geométricos y de OCR
- BBox debe tener coordenadas x1, y1, x2, y2
- OCRResult debe incluir texto, bbox y confianza
- Todos los modelos deben ser inmutables y validables

PLANIFICAR:
- Usar Pydantic v2 con BaseModel
- Añadir validadores personalizados donde necesario
- Incluir ejemplos en docstrings
- Field con alias para compatibilidad JSON

DISEÑAR:
```python
from pydantic import BaseModel, Field, validator
from typing import Optional

class BBox(BaseModel):
    """Bounding box de una región en el documento"""
    x1: int = Field(..., ge=0, description="Coordenada x superior izquierda")
    y1: int = Field(..., ge=0, description="Coordenada y superior izquierda")
    x2: int = Field(..., ge=0, description="Coordenada x inferior derecha")
    y2: int = Field(..., ge=0, description="Coordenada y inferior derecha")
    
    @validator('x2')
    def x2_must_be_greater_than_x1(cls, v, values):
        if 'x1' in values and v <= values['x1']:
            raise ValueError('x2 debe ser mayor que x1')
        return v
    
    # Similar para y2
    
    def area(self) -> int:
        """Calcula área del bounding box"""
        return (self.x2 - self.x1) * (self.y2 - self.y1)
    
    class Config:
        frozen = True  # Inmutable
```

IMPLEMENTAR:
[Código completo con todos los modelos]

TESTEAR:
```python
def test_bbox_valid():
    bbox = BBox(x1=10, y1=20, x2=100, y2=200)
    assert bbox.area() == 90 * 180

def test_bbox_invalid_x2():
    with pytest.raises(ValidationError):
        BBox(x1=100, y1=20, x2=50, y2=200)
```

VALIDAR:
- ✓ Todos los modelos validan correctamente
- ✓ Validadores custom funcionan
- ✓ Tests pasan
```

**Entregables Fase 2:**
- [ ] Modelos base implementados y testeados
- [ ] Schemas de 4 tipos de documentos
- [ ] Modelos de validación
- [ ] Suite de tests unitarios >90% cobertura

---

### **FASE 3: Input Handler** 📥

**Objetivo:** Implementar carga y preprocesamiento de documentos

**Tareas:**
1. Implementar `DocumentLoader` (`src/input/loader.py`)
   - `load_image()`: Cargar JPG, PNG, TIFF
   - `load_pdf()`: Cargar PDF y convertir a imágenes
   - `validate_document()`: Validar formato y tamaño

2. Implementar `ImagePreprocessor` (`src/input/preprocessor.py`)
   - `denoise()`: Reducir ruido
   - `deskew()`: Corregir inclinación
   - `enhance_contrast()`: Mejorar contraste (CLAHE)
   - `binarize()`: Binarización adaptativa

3. Implementar validador de entrada (`src/input/validator.py`)
   - Validar formato de archivo
   - Validar tamaño (<20MB)
   - Validar resolución (>150 DPI)

**Chain-of-Thought para Tarea 2 (Preprocesamiento):**

```
ENTENDER:
- El preprocesamiento mejora la calidad de OCR
- OpenCV es la librería estándar para esto
- Necesito: denoise, deskew, enhance_contrast, binarize
- Debe ser configurable desde config.yaml

PLANIFICAR:
- Clase ImagePreprocessor con métodos independientes
- Cada método recibe np.ndarray y retorna np.ndarray
- Parámetros configurables (fuerza denoise, umbral deskew)
- Pipeline de preprocesamiento configurable

DISEÑAR:
```python
import cv2
import numpy as np
from typing import Optional
from ..core.config import Config

class ImagePreprocessor:
    """Preprocesa imágenes para mejorar OCR"""
    
    def __init__(self, config: Config):
        self.config = config
        self.denoise_enabled = config.preprocessing.denoise
        self.denoise_strength = config.preprocessing.denoise_strength
        # ...
    
    def denoise(self, image: np.ndarray) -> np.ndarray:
        """
        Reduce ruido usando Non-Local Means Denoising
        
        Args:
            image: Imagen de entrada (BGR o Grayscale)
            
        Returns:
            Imagen sin ruido
            
        Raises:
            ValueError: Si la imagen es inválida
        """
        if image is None or image.size == 0:
            raise ValueError("Imagen inválida")
        
        # Convertir a grayscale si es necesario
        if len(image.shape) == 3:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = image
        
        # Aplicar denoising
        denoised = cv2.fastNlMeansDenoising(
            gray,
            None,
            h=self.denoise_strength,
            templateWindowSize=7,
            searchWindowSize=21
        )
        
        return denoised
    
    def deskew(self, image: np.ndarray) -> np.ndarray:
        """
        Corrige inclinación del documento
        
        Pasos:
        1. Detectar líneas con HoughLines
        2. Calcular ángulo medio de inclinación
        3. Rotar imagen para corregir
        """
        # Detectar bordes
        edges = cv2.Canny(image, 50, 150, apertureSize=3)
        
        # Detectar líneas
        lines = cv2.HoughLines(edges, 1, np.pi/180, 200)
        
        if lines is None:
            return image
        
        # Calcular ángulo medio
        angles = []
        for rho, theta in lines[:, 0]:
            angle = np.degrees(theta) - 90
            angles.append(angle)
        
        median_angle = np.median(angles)
        
        # Rotar si el ángulo supera el umbral
        if abs(median_angle) > self.config.preprocessing.deskew_threshold:
            (h, w) = image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, median_angle, 1.0)
            rotated = cv2.warpAffine(
                image, M, (w, h),
                flags=cv2.INTER_CUBIC,
                borderMode=cv2.BORDER_REPLICATE
            )
            return rotated
        
        return image
    
    def enhance_contrast(self, image: np.ndarray) -> np.ndarray:
        """
        Mejora contraste usando CLAHE
        (Contrast Limited Adaptive Histogram Equalization)
        """
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(image)
        return enhanced
    
    def binarize(self, image: np.ndarray) -> np.ndarray:
        """
        Binarización adaptativa (Otsu's method)
        """
        _, binary = cv2.threshold(
            image, 0, 255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
        return binary
    
    def preprocess_pipeline(self, image: np.ndarray) -> np.ndarray:
        """
        Ejecuta pipeline completo de preprocesamiento
        según configuración
        """
        processed = image.copy()
        
        if self.denoise_enabled:
            processed = self.denoise(processed)
        
        if self.config.preprocessing.deskew:
            processed = self.deskew(processed)
        
        if self.config.preprocessing.enhance_contrast:
            processed = self.enhance_contrast(processed)
        
        if self.config.preprocessing.binarize:
            processed = self.binarize(processed)
        
        return processed
```

IMPLEMENTAR:
[Código completo con todos los métodos]

TESTEAR:
```python
import pytest
import numpy as np
import cv2

@pytest.fixture
def sample_image():
    """Crea imagen de prueba con ruido"""
    img = np.ones((100, 100), dtype=np.uint8) * 255
    # Añadir texto simulado
    cv2.putText(img, "TEST", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2)
    # Añadir ruido
    noise = np.random.randint(0, 50, (100, 100), dtype=np.uint8)
    noisy = cv2.add(img, noise)
    return noisy

@pytest.fixture
def preprocessor(config):
    return ImagePreprocessor(config)

def test_denoise_reduces_noise(preprocessor, sample_image):
    """Test que denoise reduce ruido"""
    denoised = preprocessor.denoise(sample_image)
    
    # Calcular varianza (menor varianza = menos ruido)
    original_var = np.var(sample_image)
    denoised_var = np.var(denoised)
    
    assert denoised_var < original_var

def test_denoise_invalid_image(preprocessor):
    """Test manejo de imagen inválida"""
    with pytest.raises(ValueError):
        preprocessor.denoise(np.array([]))

def test_deskew_corrects_rotation(preprocessor):
    """Test que deskew corrige inclinación"""
    # Crear imagen rotada
    img = np.ones((100, 100), dtype=np.uint8) * 255
    cv2.line(img, (0, 0), (100, 100), 0, 2)
    
    # Rotar 5 grados
    M = cv2.getRotationMatrix2D((50, 50), 5, 1.0)
    rotated = cv2.warpAffine(img, M, (100, 100))
    
    # Corregir
    corrected = preprocessor.deskew(rotated)
    
    # Verificar que se corrigió (esto es aproximado)
    assert corrected is not None

def test_enhance_contrast_improves_histogram(preprocessor, sample_image):
    """Test que enhance_contrast mejora el histograma"""
    enhanced = preprocessor.enhance_contrast(sample_image)
    
    # Calcular rango del histograma
    orig_range = np.max(sample_image) - np.min(sample_image)
    enhanced_range = np.max(enhanced) - np.min(enhanced)
    
    # El rango debería aumentar (mejor contraste)
    assert enhanced_range >= orig_range

def test_preprocess_pipeline_integration(preprocessor, sample_image):
    """Test del pipeline completo"""
    processed = preprocessor.preprocess_pipeline(sample_image)
    
    # Verificar que la imagen fue procesada
    assert processed.shape == sample_image.shape
    assert not np.array_equal(processed, sample_image)

def test_binarize_produces_binary_image(preprocessor, sample_image):
    """Test que binarize produce solo valores 0 y 255"""
    binary = preprocessor.binarize(sample_image)
    
    unique_values = np.unique(binary)
    assert len(unique_values) <= 2
    assert all(v in [0, 255] for v in unique_values)
```

VALIDAR:
- ✓ Todos los métodos implementados
- ✓ Manejo de errores robusto
- ✓ Tests pasan (>95% cobertura)
- ✓ Performance aceptable (<1s por imagen)
```

**Entregables Fase 3:**
- [ ] DocumentLoader completo y testeado
- [ ] ImagePreprocessor con 4+ métodos
- [ ] Validador de entrada
- [ ] Tests unitarios + tests de integración
- [ ] Documentación con ejemplos

---

### **FASE 4: OCR Engine** 🔍

**Objetivo:** Implementar motores OCR (PaddleOCR + Tesseract)

**Tareas:**
1. Implementar `PaddleOCREngine` (`src/ocr/paddle_engine.py`)
   - Inicializar PaddleOCR con config
   - `extract_text()`: Texto completo con coordenadas
   - `extract_table()`: Extraer tablas como DataFrame
   - `extract_region()`: Texto de región específica

2. Implementar `TesseractEngine` (`src/ocr/tesseract_engine.py`)
   - Configurar Tesseract (PSM, OEM)
   - `extract_text()`: Fallback cuando PaddleOCR falla

3. Implementar `TableDetector` (`src/ocr/table_detector.py`)
   - `detect_tables()`: Ubicación de tablas
   - `extract_table_cells()`: Celdas individuales

4. Implementar `RegionExtractor` (`src/ocr/region_extractor.py`)
   - `extract_header()`: Región de cabecera
   - `extract_footer()`: Región de pie
   - `detect_stamps()`: Detectar sellos
   - `detect_signatures()`: Detectar firmas

**Chain-of-Thought para Tarea 1:**

```
ENTENDER:
- PaddleOCR es el motor principal de OCR
- Debe configurarse para español sin GPU (MVP)
- Necesito extraer texto con coordenadas para validación
- Debe manejar errores y proporcionar fallback

PLANIFICAR:
- Singleton pattern para no reinicializar PaddleOCR
- Cache de resultados para documentos procesados múltiples veces
- Logging detallado de confianza de OCR
- Retry logic para fallos temporales

DISEÑAR:
```python
from paddleocr import PaddleOCR
import numpy as np
from typing import List, Optional
from ..models.document import OCRResult, BBox
from ..core.logger import get_logger
from ..core.config import Config

class PaddleOCREngine:
    """Motor de OCR usando PaddleOCR"""
    
    _instance = None
    
    def __new__(cls, config: Config):
        """Implementa singleton"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, config: Config):
        """
        Inicializa PaddleOCR
        
        Args:
            config: Configuración del sistema
        """
        if self._initialized:
            return
        
        self.config = config
        self.logger = get_logger(__name__)
        
        self.logger.info("Inicializando PaddleOCR...")
        
        try:
            self.ocr = PaddleOCR(
                use_angle_cls=config.ocr.paddleocr.use_angle_cls,
                lang=config.ocr.language,
                use_gpu=config.ocr.use_gpu,
                show_log=False,
                det_db_thresh=config.ocr.paddleocr.det_db_thresh,
                det_db_box_thresh=config.ocr.paddleocr.det_db_box_thresh,
                det_db_unclip_ratio=config.ocr.paddleocr.det_db_unclip_ratio
            )
            
            self._initialized = True
            self.logger.info("PaddleOCR inicializado correctamente")
            
        except Exception as e:
            self.logger.error(f"Error inicializando PaddleOCR: {e}")
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
            ValueError: Si la imagen es inválida
            RuntimeError: Si el OCR falla
        """
        if image is None or image.size == 0:
            raise ValueError("Imagen inválida para OCR")
        
        threshold = confidence_threshold or self.config.ocr.confidence_threshold
        
        self.logger.debug(f"Ejecutando OCR (umbral confianza: {threshold})")
        
        try:
            # Ejecutar OCR
            result = self.ocr.ocr(image, cls=True)
            
            if not result or not result[0]:
                self.logger.warning("OCR no detectó texto en la imagen")
                return []
            
            # Parsear resultados
            ocr_results = []
            
            for line in result[0]:
                bbox_coords = line[0]
                text_info = line[1]
                text = text_info[0]
                confidence = text_info[1]
                
                # Filtrar por confianza
                if confidence < threshold:
                    self.logger.debug(
                        f"Texto '{text}' descartado (confianza: {confidence:.2f})"
                    )
                    continue
                
                # Crear BBox
                # bbox_coords es [[x1,y1], [x2,y1], [x2,y2], [x1,y2]]
                x_coords = [point[0] for point in bbox_coords]
                y_coords = [point[1] for point in bbox_coords]
                
                bbox = BBox(
                    x1=int(min(x_coords)),
                    y1=int(min(y_coords)),
                    x2=int(max(x_coords)),
                    y2=int(max(y_coords))
                )
                
                ocr_result = OCRResult(
                    text=text,
                    bbox=bbox,
                    confidence=confidence
                )
                
                ocr_results.append(ocr_result)
            
            # Logging de resumen
            avg_confidence = np.mean([r.confidence for r in ocr_results]) if ocr_results else 0
            self.logger.info(
                f"OCR completado: {len(ocr_results)} líneas detectadas, "
                f"confianza promedio: {avg_confidence:.2%}"
            )
            
            return ocr_results
            
        except Exception as e:
            self.logger.error(f"Error durante OCR: {e}")
            raise RuntimeError(f"Fallo en OCR: {e}")
    
    def extract_region(
        self, 
        image: np.ndarray, 
        bbox: BBox
    ) -> str:
        """
        Extrae texto de una región específica
        
        Args:
            image: Imagen completa
            bbox: Región de interés
            
        Returns:
            Texto extraído de la región
        """
        # Recortar región
        region = image[bbox.y1:bbox.y2, bbox.x1:bbox.x2]
        
        # Ejecutar OCR en región
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
        Extrae tabla de documento y retorna DataFrame
        
        Args:
            image: Imagen del documento
            table_bbox: BBox de la tabla (None = detectar automáticamente)
            
        Returns:
            DataFrame con contenido de la tabla
        """
        from paddleocr import PPStructure
        
        # Si no hay bbox, usar toda la imagen
        if table_bbox:
            table_image = image[
                table_bbox.y1:table_bbox.y2,
                table_bbox.x1:table_bbox.x2
            ]
        else:
            table_image = image
        
        # Usar PPStructure para extraer tabla
        table_engine = PPStructure(show_log=False, lang=self.config.ocr.language)
        result = table_engine(table_image)
        
        # Parsear resultado a DataFrame
        # [Implementación de parsing]
        
        return df
    
    def calculate_average_confidence(
        self, 
        ocr_results: List[OCRResult]
    ) -> float:
        """Calcula confianza promedio de resultados OCR"""
        if not ocr_results:
            return 0.0
        
        confidences = [r.confidence for r in ocr_results]
        return float(np.mean(confidences))
```

IMPLEMENTAR:
[Código completo con todos los métodos y clases]

TESTEAR:
```python
import pytest
from unittest.mock import Mock, patch
import numpy as np

@pytest.fixture
def sample_document_image():
    """Crea imagen de documento simulado"""
    img = np.ones((1000, 800, 3), dtype=np.uint8) * 255
    # Añadir texto simulado
    cv2.putText(img, "ALBARAN N: ALB-20250115", (50, 100), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2)
    cv2.putText(img, "Fecha: 2025-01-15", (50, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 1, 0, 2)
    return img

@pytest.fixture
def paddle_engine(config):
    return PaddleOCREngine(config)

def test_paddle_engine_singleton(config):
    """Test que PaddleOCREngine es singleton"""
    engine1 = PaddleOCREngine(config)
    engine2 = PaddleOCREngine(config)
    assert engine1 is engine2

def test_extract_text_returns_results(paddle_engine, sample_document_image):
    """Test extracción de texto básica"""
    results = paddle_engine.extract_text(sample_document_image)
    
    assert isinstance(results, list)
    assert len(results) > 0
    assert all(isinstance(r, OCRResult) for r in results)

def test_extract_text_filters_low_confidence(paddle_engine, sample_document_image):
    """Test filtrado por confianza"""
    # Con umbral bajo
    results_low = paddle_engine.extract_text(
        sample_document_image, 
        confidence_threshold=0.5
    )
    
    # Con umbral alto
    results_high = paddle_engine.extract_text(
        sample_document_image,
        confidence_threshold=0.9
    )
    
    # Debe haber menos resultados con umbral alto
    assert len(results_high) <= len(results_low)

def test_extract_text_invalid_image(paddle_engine):
    """Test manejo de imagen inválida"""
    with pytest.raises(ValueError):
        paddle_engine.extract_text(np.array([]))

@patch('paddleocr.PaddleOCR')
def test_extract_text_handles_ocr_failure(mock_paddle, config):
    """Test manejo de fallo en OCR"""
    mock_paddle.return_value.ocr.side_effect = Exception("OCR failed")
    
    engine = PaddleOCREngine(config)
    
    with pytest.raises(RuntimeError):
        engine.extract_text(np.ones((100, 100, 3), dtype=np.uint8))

def test_extract_region(paddle_engine, sample_document_image):
    """Test extracción de región específica"""
    # Definir región de cabecera
    bbox = BBox(x1=0, y1=0, x2=800, y2=200)
    
    text = paddle_engine.extract_region(sample_document_image, bbox)
    
    assert isinstance(text, str)
    assert len(text) > 0

def test_calculate_average_confidence(paddle_engine):
    """Test cálculo de confianza promedio"""
    results = [
        OCRResult(text="test1", bbox=BBox(0, 0, 10, 10), confidence=0.9),
        OCRResult(text="test2", bbox=BBox(0, 0, 10, 10), confidence=0.8),
    ]
    
    avg = paddle_engine.calculate_average_confidence(results)
    assert avg == 0.85

def test_calculate_average_confidence_empty(paddle_engine):
    """Test confianza con lista vacía"""
    avg = paddle_engine.calculate_average_confidence([])
    assert avg == 0.0
```

VALIDAR:
- ✓ PaddleOCR inicializado correctamente
- ✓ Extracción de texto funciona
- ✓ Filtrado por confianza correcto
- ✓ Manejo de errores robusto
- ✓ Tests pasan (>90% cobertura)
```

**Entregables Fase 4:**
- [ ] PaddleOCREngine completo
- [ ] TesseractEngine como fallback
- [ ] TableDetector funcional
- [ ] RegionExtractor implementado
- [ ] Suite completa de tests
- [ ] Benchmarks de performance

---

### **FASE 5: LLM Engine** 🤖

**Objetivo:** Implementar clasificación y extracción con LLM local

**Tareas:**
1. Implementar `OllamaClient` (`src/llm/ollama_client.py`)
   - Conexión con Ollama
   - Método `generate()` básico
   - Método `generate_json()` con schema
   - Retry logic y timeout

2. Crear templates de prompts (`src/llm/prompts.py`)
   - Prompt de clasificación
   - Prompts de extracción por tipo de documento
   - Prompts de resolución de ambigüedades

3. Implementar `DocumentClassifier` (`src/llm/classifier.py`)
   - Clasificar en 4 tipos
   - Nivel de confianza
   - Fallback si confianza baja

4. Implementar `FieldExtractor` (`src/llm/extractor.py`)
   - Extracción según templates
   - Validación de schema
   - Normalización de datos

**Chain-of-Thought para Tarea 4:**

```
ENTENDER:
- FieldExtractor usa LLM para extraer campos estructurados
- Necesita templates específicos por tipo de documento
- Debe validar con schemas Pydantic
- Debe normalizar formatos (fechas, números, etc.)

PLANIFICAR:
- Cargar templates desde archivos YAML
- Generar prompt dinámicamente según tipo
- Usar JSON mode de LLM para output estructurado
- Validar con Pydantic y reintentar si falla

DISEÑAR:
```python
from typing import Dict, Any, Optional
import yaml
from pathlib import Path
from pydantic import ValidationError
from ..models.schemas import *
from ..llm.ollama_client import OllamaClient
from ..llm.prompts import EXTRACTION_PROMPTS
from ..core.logger import get_logger

class FieldExtractor:
    """Extrae campos estructurados usando LLM"""
    
    def __init__(self, llm_client: OllamaClient, templates_dir: Path):
        """
        Args:
            llm_client: Cliente de Ollama configurado
            templates_dir: Directorio con templates YAML
        """
        self.llm = llm_client
        self.templates_dir = templates_dir
        self.logger = get_logger(__name__)
        
        # Cargar templates
        self.templates = self._load_templates()
        
        # Mapeo de tipos a schemas
        self.schema_map = {
            "ALBARAN": AlbaranSchema,
            "ORDEN_ENVIO": OrdenEnvioSchema,
            "NOTA_RECEPCION": NotaRecepcionSchema,
            "PARTE_TRANSPORTE": ParteTransporteSchema
        }
    
    def _load_templates(self) -> Dict[str, dict]:
        """Carga templates YAML de tipos de documento"""
        templates = {}
        
        for template_file in self.templates_dir.glob("*.yaml"):
            doc_type = template_file.stem.upper()
            with open(template_file, 'r', encoding='utf-8') as f:
                templates[doc_type] = yaml.safe_load(f)
        
        self.logger.info(f"Templates cargados: {list(templates.keys())}")
        return templates
    
    def extract_fields(
        self,
        ocr_text: str,
        doc_type: str,
        ocr_results: Optional[List[OCRResult]] = None,
        max_retries: int = 3
    ) -> Dict[str, Any]:
        """
        Extrae campos estructurados del texto OCR
        
        Args:
            ocr_text: Texto completo extraído por OCR
            doc_type: Tipo de documento (ALBARAN, ORDEN_ENVIO, etc.)
            ocr_results: Resultados OCR detallados (opcional)
            max_retries: Intentos máximos si falla validación
            
        Returns:
            Diccionario con campos extraídos y validados
            
        Raises:
            ValueError: Si el tipo de documento no es válido
            RuntimeError: Si la extracción falla después de todos los intentos
        """
        if doc_type not in self.schema_map:
            raise ValueError(f"Tipo de documento inválido: {doc_type}")
        
        template = self.templates[doc_type]
        schema_class = self.schema_map[doc_type]
        
        self.logger.info(f"Extrayendo campos para {doc_type}")
        
        # Generar prompt
        prompt = self._generate_extraction_prompt(
            ocr_text=ocr_text,
            template=template,
            doc_type=doc_type
        )
        
        # Intentar extracción con reintentos
        for attempt in range(1, max_retries + 1):
            try:
                self.logger.debug(f"Intento {attempt}/{max_retries}")
                
                # Generar JSON con LLM
                extracted_data = self.llm.generate_json(
                    prompt=prompt,
                    schema=self._get_json_schema(template)
                )
                
                # Validar con Pydantic
                validated_data = schema_class(**extracted_data)
                
                self.logger.info(
                    f"Extracción exitosa: {len(extracted_data)} campos"
                )
                
                return validated_data.dict()
                
            except ValidationError as e:
                self.logger.warning(
                    f"Intento {attempt} falló en validación: {e}"
                )
                
                if attempt < max_retries:
                    # Añadir errores al prompt para próximo intento
                    prompt = self._add_validation_errors_to_prompt(
                        prompt, e
                    )
                else:
                    raise RuntimeError(
                        f"Extracción falló después de {max_retries} intentos: {e}"
                    )
            
            except Exception as e:
                self.logger.error(f"Error en extracción: {e}")
                raise RuntimeError(f"Error durante extracción: {e}")
    
    def _generate_extraction_prompt(
        self,
        ocr_text: str,
        template: dict,
        doc_type: str
    ) -> str:
        """
        Genera prompt de extracción basado en el template
        
        Incluye:
        - Instrucciones específicas del tipo de documento
        - Lista de campos obligatorios y opcionales
        - Ejemplos de valores esperados
        - Formato JSON esperado
        """
        prompt_template = EXTRACTION_PROMPTS[doc_type]
        
        # Listar campos obligatorios
        required_fields = []
        for field_name, field_spec in template['campos_obligatorios'].items():
            required_fields.append(
                f"- {field_name}: {field_spec['tipo']} - {field_spec.get('descripcion', '')}"
            )
        
        required_fields_str = "\n".join(required_fields)
        
        # Formatear prompt
        prompt = prompt_template.format(
            ocr_text=ocr_text,
            required_fields=required_fields_str
        )
        
        return prompt
    
    def _get_json_schema(self, template: dict) -> dict:
        """Convierte template YAML a JSON schema para el LLM"""
        schema = {
            "type": "object",
            "properties": {},
            "required": []
        }
        
        for field_name, field_spec in template['campos_obligatorios'].items():
            schema["properties"][field_name] = {
                "type": self._yaml_type_to_json_type(field_spec['tipo'])
            }
            
            if not field_spec.get('opcional', False):
                schema["required"].append(field_name)
        
        return schema
    
    def _yaml_type_to_json_type(self, yaml_type: str) -> str:
        """Mapea tipos YAML a tipos JSON"""
        mapping = {
            "string": "string",
            "integer": "integer",
            "float": "number",
            "date": "string",
            "datetime": "string",
            "boolean": "boolean",
            "array": "array"
        }
        return mapping.get(yaml_type, "string")
    
    def _add_validation_errors_to_prompt(
        self,
        original_prompt: str,
        error: ValidationError
    ) -> str:
        """
        Añade errores de validación al prompt para retry
        
        Esto ayuda al LLM a corregir los errores específicos
        """
        error_messages = []
        for err in error.errors():
            field = ".".join(str(loc) for loc in err['loc'])
            msg = err['msg']
            error_messages.append(f"- Campo '{field}': {msg}")
        
        errors_str = "\n".join(error_messages)
        
        retry_prompt = f"""{original_prompt}

IMPORTANTE: El intento anterior tuvo los siguientes errores de validación.
Por favor, corrígelos en esta respuesta:

{errors_str}

Responde nuevamente con el JSON corregido.
"""
        
        return retry_prompt
    
    def resolve_ambiguity(
        self,
        field_name: str,
        candidates: List[str],
        context: str
    ) -> str:
        """
        Resuelve ambigüedades cuando hay múltiples valores posibles
        
        Args:
            field_name: Nombre del campo ambiguo
            candidates: Lista de valores posibles
            context: Contexto del documento
            
        Returns:
            Valor más probable
        """
        prompt = f"""
Tengo ambigüedad en el campo '{field_name}' de un documento logístico.

Valores posibles detectados por OCR:
{chr(10).join(f'- {c}' for c in candidates)}

Contexto del documento:
{context}

¿Cuál es el valor más probable para '{field_name}'?
Responde SOLO con el valor, sin explicaciones.
"""
        
        resolved = self.llm.generate(prompt).strip()
        
        self.logger.info(
            f"Ambigüedad resuelta para '{field_name}': {resolved}"
        )
        
        return resolved
    
    def normalize_date(self, date_str: str) -> str:
        """Normaliza fechas a formato ISO (YYYY-MM-DD)"""
        from dateutil import parser
        
        try:
            parsed = parser.parse(date_str, dayfirst=True)
            return parsed.strftime("%Y-%m-%d")
        except Exception as e:
            self.logger.warning(f"No se pudo parsear fecha '{date_str}': {e}")
            return date_str
    
    def normalize_number(self, number_str: str) -> float:
        """Normaliza números (maneja formatos europeos/americanos)"""
        # Remover separadores de miles
        cleaned = number_str.replace('.', '').replace(',', '.')
        
        try:
            return float(cleaned)
        except ValueError:
            self.logger.warning(f"No se pudo parsear número '{number_str}'")
            return 0.0
```

IMPLEMENTAR:
[Código completo]

TESTEAR:
```python
import pytest
from unittest.mock import Mock, MagicMock
from pydantic import ValidationError

@pytest.fixture
def ollama_client():
    """Mock de OllamaClient"""
    mock = Mock(spec=OllamaClient)
    return mock

@pytest.fixture
def extractor(ollama_client, tmp_path):
    """Crea FieldExtractor con templates de prueba"""
    # Crear template de prueba
    template_content = """
nombre: Albarán de Entrega
descripcion: Documento de entrega

campos_obligatorios:
  numero_albaran:
    tipo: string
    patron: "^ALB-\\d{8}$"
  fecha_emision:
    tipo: date
    formato: "YYYY-MM-DD"
  total:
    tipo: float
"""
    
    template_file = tmp_path / "albaran.yaml"
    template_file.write_text(template_content)
    
    return FieldExtractor(ollama_client, tmp_path)

def test_extract_fields_success(extractor, ollama_client):
    """Test extracción exitosa"""
    # Mock respuesta del LLM
    ollama_client.generate_json.return_value = {
        "numero_albaran": "ALB-20250115",
        "fecha_emision": "2025-01-15",
        "total": 429.00
    }
    
    ocr_text = "ALBARAN ALB-20250115 Fecha: 15/01/2025 Total: 429,00"
    
    result = extractor.extract_fields(ocr_text, "ALBARAN")
    
    assert result["numero_albaran"] == "ALB-20250115"
    assert result["total"] == 429.00

def test_extract_fields_retry_on_validation_error(extractor, ollama_client):
    """Test retry cuando hay error de validación"""
    # Primera llamada falla, segunda funciona
    ollama_client.generate_json.side_effect = [
        {"numero_albaran": "INVALID"},  # Falla validación
        {"numero_albaran": "ALB-20250115", "fecha_emision": "2025-01-15", "total": 100.0}
    ]
    
    ocr_text = "Test"
    result = extractor.extract_fields(ocr_text, "ALBARAN", max_retries=2)
    
    assert result["numero_albaran"] == "ALB-20250115"
    assert ollama_client.generate_json.call_count == 2

def test_extract_fields_max_retries_exceeded(extractor, ollama_client):
    """Test fallo después de máximo de reintentos"""
    ollama_client.generate_json.return_value = {"numero_albaran": "INVALID"}
    
    with pytest.raises(RuntimeError):
        extractor.extract_fields("Test", "ALBARAN", max_retries=3)

def test_resolve_ambiguity(extractor, ollama_client):
    """Test resolución de ambigüedad"""
    ollama_client.generate.return_value = "O123"
    
    resolved = extractor.resolve_ambiguity(
        field_name="codigo_producto",
        candidates=["0123", "O123", "Q123"],
        context="Producto farmacéutico"
    )
    
    assert resolved == "O123"

def test_normalize_date(extractor):
    """Test normalización de fechas"""
    assert extractor.normalize_date("15/01/2025") == "2025-01-15"
    assert extractor.normalize_date("01-15-2025") == "2025-01-15"
    assert extractor.normalize_date("2025-01-15") == "2025-01-15"

def test_normalize_number(extractor):
    """Test normalización de números"""
    assert extractor.normalize_number("1.234,56") == 1234.56
    assert extractor.normalize_number("1,234.56") == 1234.56
    assert extractor.normalize_number("1234.56") == 1234.56

@pytest.mark.integration
def test_full_extraction_pipeline(extractor, ollama_client):
    """Test integración completa de extracción"""
    # [Test con documento real]
    pass
```

VALIDAR:
- ✓ Extracción funciona con LLM real
- ✓ Reintentos manejan errores
- ✓ Normalización correcta
- ✓ Tests pasan
```

**Entregables Fase 5:**
- [ ] OllamaClient con retry logic
- [ ] Templates de prompts completos
- [ ] DocumentClassifier >90% accuracy
- [ ] FieldExtractor con validación
- [ ] Tests unitarios + integración
- [ ] Benchmarks de latencia

---

### **FASE 6: Validator Engine** ✅

**Objetivo:** Implementar validación individual y cruzada

**Tareas:**
1. Implementar `CrossValidator` (`src/validator/cross_validator.py`)
   - Agrupar documentos relacionados
   - Validar grupo completo

2. Implementar `RulesEngine` (`src/validator/rules_engine.py`)
   - Reglas de cantidades
   - Reglas de códigos
   - Reglas de fechas

3. Implementar `DiscrepancyDetector` (`src/validator/discrepancy_detector.py`)
   - Detectar tipos de discrepancias
   - Calcular severidad
   - Generar descripciones

**Entregables Fase 6:**
- [ ] CrossValidator funcional
- [ ] 10+ reglas de negocio
- [ ] Detección de discrepancias >75% recall
- [ ] Tests exhaustivos

---

### **FASE 7: Pipeline Principal** 🔄

**Objetivo:** Orquestar todos los componentes

**Tareas:**
1. Implementar `DocumentProcessingPipeline` (`src/core/pipeline.py`)
   - Flujo end-to-end
   - Manejo de errores robusto
   - Logging detallado
   - Métricas de performance

2. Implementar manejo de estado
3. Implementar cache de resultados

**Entregables Fase 7:**
- [ ] Pipeline completo funcional
- [ ] Procesamiento <30s por documento
- [ ] Manejo de errores robusto
- [ ] Tests de integración

---

### **FASE 8: CLI** 💻

**Objetivo:** Interfaz de línea de comandos completa

**Tareas:**
1. Implementar comandos con Typer (`src/main.py`)
   - `process`: Procesar documento individual
   - `batch`: Procesar lote
   - `validate`: Validación cruzada
   - `evaluate`: Evaluación con ground truth
   - `config`: Gestión de configuración

2. Implementar progress bars y output formateado

**Entregables Fase 8:**
- [ ] CLI completa y documentada
- [ ] Help text detallado
- [ ] Output user-friendly
- [ ] Tests de CLI

---

### **FASE 9: Testing y Evaluación** 🧪

**Objetivo:** Suite completa de tests y evaluación de métricas

**Tareas:**
1. Tests unitarios (>90% cobertura)
2. Tests de integración
3. Tests end-to-end con datos reales
4. Evaluación en dataset de 50 documentos
5. Generación de reportes de métricas

**Entregables Fase 9:**
- [ ] Cobertura >90%
- [ ] Todos los tests pasan
- [ ] Reporte de evaluación
- [ ] Métricas documentadas

---

### **FASE 10: Documentación** 📚

**Objetivo:** Documentación completa del sistema

**Tareas:**
1. README.md con guía de instalación
2. Documentación de arquitectura
3. Guía de uso con ejemplos
4. Documentación de API interna
5. Troubleshooting guide

**Entregables Fase 10:**
- [ ] Documentación completa
- [ ] Ejemplos funcionales
- [ ] Guías paso a paso

---

## 🎓 PRINCIPIOS DE DESARROLLO

Durante todo el desarrollo, sigue estos principios:

### 1. **Test-Driven Development (TDD)**
- Escribe tests ANTES de implementar
- Ejecuta tests constantemente
- Mantén cobertura >90%

### 2. **Clean Code**
- Nombres descriptivos
- Funciones pequeñas y enfocadas
- Documentación clara
- Type hints siempre

### 3. **Error Handling**
- Nunca ignorar excepciones
- Logging apropiado
- Mensajes de error útiles
- Graceful degradation

### 4. **Performance**
- Profile antes de optimizar
- Cache cuando apropiado
- Evitar operaciones costosas innecesarias
- Documentar trade-offs

### 5. **Mantenibilidad**
- Código modular
- Bajo acoplamiento
- Alta cohesión
- SOLID principles

---

## 📊 MÉTRICAS DE CALIDAD

Valida que tu implementación cumple:

- [ ] **Tests:** >90% cobertura de código
- [ ] **Performance:** <30s procesamiento por documento
- [ ] **OCR Accuracy:** >85%
- [ ] **Clasificación:** >90% accuracy
- [ ] **Extracción:** >80% F1-score
- [ ] **Validación:** >75% recall en discrepancias
- [ ] **Linting:** 0 errores en pylint/flake8
- [ ] **Type Checking:** 0 errores en mypy
- [ ] **Documentación:** Todos los módulos documentados

---

## 🚀 EJEMPLO DE EJECUCIÓN COMPLETA

Al final de todo el desarrollo, deberías poder ejecutar:

```bash
# Setup
python scripts/setup_project_structure.py
pip install -r requirements.txt
ollama pull llama3:8b

# Procesar documento
python src/main.py process \
  --file data/raw/albaran_001.pdf \
  --output data/processed/albaran_001.json \
  --verbose

# Validar grupo
python src/main.py validate \
  --group data/processed/grupo_pedido_12345/*.json \
  --report data/results/validation_report.json

# Evaluar sistema
python src/main.py evaluate \
  --test-dir data/test/ \
  --ground-truth data/test/ground_truth.json \
  --metrics-output data/results/metrics.json

# Ver resultados
python scripts/generate_evaluation_report.py
```

---

## 💡 TIPS FINALES

1. **Trabaja incrementalmente**: No intentes hacer todo a la vez
2. **Tests primero**: Más fácil refactorizar con buena cobertura
3. **Logging es tu amigo**: Debug será mucho más fácil
4. **Documenta decisiones**: Especialmente trade-offs y limitaciones
5. **Mide antes de optimizar**: Profile para saber dónde optimizar
6. **Pide ayuda cuando lo necesites**: No te quedes bloqueado

---

## 📝 TEMPLATE DE COMMIT MESSAGES

Usa commits descriptivos siguiendo conventional commits:

```
feat(ocr): implementar PaddleOCREngine con detección de tablas
fix(validator): corregir validación de fechas en secuencia
test(llm): añadir tests de integración para extracción
docs(readme): actualizar guía de instalación
refactor(pipeline): simplificar manejo de errores
perf(ocr): optimizar preprocesamiento de imágenes
```

---

## ✅ CHECKLIST FINAL

Antes de considerar el MVP completo, verifica:

- [ ] Todos los componentes implementados según SRS
- [ ] Suite completa de tests (unitarios + integración)
- [ ] Cobertura de tests >90%
- [ ] Todos los tests pasan
- [ ] CLI funcional con todos los comandos
- [ ] Documentación completa
- [ ] Evaluación ejecutada en dataset de prueba
- [ ] Métricas cumplen objetivos (OCR >85%, Clasificación >90%, etc.)
- [ ] Código limpio y bien documentado
- [ ] Sin code smells críticos
- [ ] Linting y type checking pasan
- [ ] README con instrucciones claras
- [ ] Ejemplos funcionales incluidos

---

## 🎯 TU MISIÓN COMIENZA AHORA

**Instrucción final para el agente Claude Code:**

Comenzando con la **FASE 1**, implementa el backend completo del sistema siguiendo metodología Chain-of-Thought. Para cada componente:

1. Piensa en voz alta sobre el diseño
2. Implementa con tests
3. Valida que funciona
4. Documenta decisiones importantes
5. Avanza a la siguiente fase

**¡Adelante y buena suerte! 🚀**

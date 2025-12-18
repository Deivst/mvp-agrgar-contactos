# Agente de Clasificación y Validación de Documentos Logísticos
## PRD (Product Requirements Document) + SRS (Software Requirements Specification)

**Versión:** 1.0  
**Fecha:** Diciembre 17, 2025  
**Proyecto:** MVP - Agente OCR/LLM para Documentación Logística  
**Entorno objetivo:** Visual Studio Code + Claude Code (Máquina Local)

---

## 1. PRODUCT REQUIREMENTS DOCUMENT (PRD)

### 1.1 Resumen Ejecutivo

**Problema:**  
La gestión manual de documentos logísticos (albaranes, órdenes de envío, notas de recepción, partes de transporte) genera errores operativos, pérdida de trazabilidad y demoras en la entrada de datos a sistemas ERP/WMS.

**Solución Propuesta:**  
Agente de IA local que automatiza la lectura, clasificación, extracción y validación de campos clave en documentación logística mediante OCR (PaddleOCR/Tesseract) y modelos de lenguaje locales (LLM), ejecutándose en Visual Studio Code con Claude Code.

**Valor Agregado:**
- Reducción de errores manuales de transcripción (>70%)
- Mejora de trazabilidad operativa documental
- Detección proactiva de discrepancias entre documentos relacionados
- Procesamiento local sin dependencias de servicios cloud

---

### 1.2 Objetivos del Producto

#### Objetivo General
Desarrollar un MVP funcional de un agente que automatice la lectura, clasificación y validación de documentos logísticos utilizando OCR y LLM locales, reduciendo errores manuales y mejorando la trazabilidad operativa.

#### Objetivos Específicos

1. **Análisis Documental**
   - Identificar formatos habituales en organizaciones logísticas tipo (almacén, distribuidora, farmacéutica)
   - Documentar campos críticos por tipo de documento
   - Crear base de conocimiento de estructuras documentales

2. **Pipeline OCR Especializado**
   - Implementar OCR con soporte para tablas, celdas, sellos y firmas
   - Integrar PaddleOCR como motor principal con fallback a Tesseract
   - Optimizar preprocesamiento de imágenes para documentos logísticos

3. **Extracción Estructurada de Campos**
   - Extraer campos clave: referencias de pedido, códigos de producto, cantidades, fechas, firmas, matrículas
   - Utilizar LLM local para resolver ambigüedades de texto
   - Generar salida estructurada en JSON

4. **Validación Cruzada de Documentos**
   - Comparar documentos relacionados (pedido ↔ albarán ↔ factura)
   - Detectar discrepancias en cantidades, códigos y referencias
   - Generar alertas de inconsistencias

5. **Evaluación de Precisión**
   - Medir accuracy del OCR por tipo de documento
   - Evaluar F1-score de extracción de campos
   - Documentar tasa de falsos positivos/negativos

6. **Documentación Técnica**
   - Documentar limitaciones identificadas
   - Proponer diseño de integración con ERP/WMS
   - Definir roadmap post-MVP

---

### 1.3 Usuarios y Casos de Uso

#### Usuarios Objetivo

1. **Operador de Almacén**
   - Digitaliza albaranes de entrada/salida
   - Valida información antes de ingresarla al WMS

2. **Responsable Logístico**
   - Supervisa discrepancias entre documentos
   - Genera reportes de trazabilidad

3. **Administrador de Sistemas**
   - Configura el agente según formatos específicos
   - Monitorea métricas de precisión

#### Casos de Uso Principales

**CU-01: Clasificación de Documento**
- **Actor:** Sistema
- **Descripción:** El agente recibe una imagen/PDF y determina su tipo (albarán, orden de envío, nota de recepción, parte de transporte)
- **Precondición:** Documento digitalizado disponible
- **Flujo:**
  1. Carga imagen/PDF
  2. Aplica OCR preliminar
  3. Analiza estructura y vocabulario con LLM
  4. Clasifica documento en una de las categorías
  5. Retorna tipo de documento + nivel de confianza
- **Postcondición:** Documento clasificado correctamente

**CU-02: Extracción de Campos Clave**
- **Actor:** Usuario
- **Descripción:** El agente extrae campos estructurados según el tipo de documento
- **Precondición:** Documento clasificado
- **Flujo:**
  1. Identifica regiones de interés (tablas, cabeceras)
  2. Aplica OCR especializado por región
  3. Extrae campos clave usando templates + LLM
  4. Valida coherencia de datos extraídos
  5. Genera JSON estructurado
- **Postcondición:** Campos extraídos en formato estructurado

**CU-03: Validación Cruzada**
- **Actor:** Usuario
- **Descripción:** El agente compara documentos relacionados y detecta discrepancias
- **Precondición:** Múltiples documentos de un mismo proceso logístico
- **Flujo:**
  1. Relaciona documentos por identificadores comunes
  2. Compara campos críticos (cantidades, códigos, fechas)
  3. Detecta discrepancias según reglas de negocio
  4. Genera reporte de inconsistencias
  5. Sugiere correcciones
- **Postcondición:** Reporte de validación generado

---

### 1.4 Requisitos Funcionales (Alto Nivel)

| ID | Requisito | Prioridad | Tipo |
|----|-----------|-----------|------|
| RF-01 | El sistema debe clasificar documentos en 4 categorías (albarán, orden envío, nota recepción, parte transporte) | CRÍTICA | Core |
| RF-02 | El sistema debe extraer al menos 10 campos clave por tipo de documento | CRÍTICA | Core |
| RF-03 | El sistema debe soportar imágenes (JPG, PNG) y PDFs | CRÍTICA | Core |
| RF-04 | El sistema debe validar cantidades entre documentos relacionados | ALTA | Core |
| RF-05 | El sistema debe detectar códigos de producto duplicados o erróneos | ALTA | Core |
| RF-06 | El sistema debe identificar firmas y sellos en los documentos | MEDIA | Enhancement |
| RF-07 | El sistema debe generar reportes de discrepancias en formato JSON | ALTA | Core |
| RF-08 | El sistema debe permitir configuración de templates por organización | MEDIA | Enhancement |
| RF-09 | El sistema debe funcionar offline sin conexión a internet | CRÍTICA | Core |
| RF-10 | El sistema debe procesar un documento en menos de 30 segundos | ALTA | Performance |

---

### 1.5 Requisitos No Funcionales (Alto Nivel)

| ID | Requisito | Prioridad |
|----|-----------|-----------|
| RNF-01 | **Precisión OCR:** >85% accuracy en texto impreso legible | CRÍTICA |
| RNF-02 | **Extracción de campos:** F1-score >80% por campo clave | CRÍTICA |
| RNF-03 | **Portabilidad:** Debe ejecutarse en Windows, macOS y Linux | ALTA |
| RNF-04 | **Recursos:** Máximo 8GB RAM, GPU opcional pero no obligatoria | ALTA |
| RNF-05 | **Escalabilidad MVP:** Hasta 100 documentos/día | MEDIA |
| RNF-06 | **Mantenibilidad:** Código modular, documentado y versionado | ALTA |
| RNF-07 | **Seguridad:** Procesamiento local, sin envío de datos externos | CRÍTICA |
| RNF-08 | **Usabilidad:** Interfaz CLI simple, logs claros | MEDIA |

---

### 1.6 Alcance del MVP

#### Dentro del Alcance (In Scope)
✅ Clasificación de 4 tipos de documentos logísticos  
✅ Extracción de 10+ campos clave por tipo  
✅ OCR con PaddleOCR y fallback a Tesseract  
✅ LLM local para resolución de ambigüedades (Llama 3, Mistral o similar)  
✅ Validación cruzada básica (cantidades, códigos)  
✅ Interfaz CLI en VS Code con Claude Code  
✅ Salida en JSON estructurado  
✅ Evaluación de métricas de precisión  
✅ Documentación técnica completa  

#### Fuera del Alcance (Out of Scope)
❌ Integración directa con ERP/WMS (se documenta como trabajo futuro)  
❌ Interfaz gráfica web o desktop  
❌ Procesamiento batch masivo (>100 docs/día)  
❌ Reconocimiento de escritura manual (manuscritos)  
❌ OCR en idiomas diferentes a español  
❌ Detección avanzada de fraude documental  
❌ API REST para terceros  
❌ Sistema de aprendizaje continuo (retraining)  

---

### 1.7 Métricas de Éxito

| Métrica | Objetivo MVP | Método de Medición |
|---------|--------------|-------------------|
| Precisión OCR | >85% | Comparación manual en dataset de prueba (50 docs) |
| F1-Score Extracción | >80% | Evaluación por campo contra ground truth |
| Clasificación Correcta | >90% | Accuracy en categorización de documentos |
| Detección Discrepancias | >75% | Recall en validación cruzada |
| Tiempo de Procesamiento | <30s/doc | Medición automática por documento |
| Tasa de Error Fatal | <5% | Documentos no procesables |

---

### 1.8 Restricciones y Dependencias

#### Restricciones
- **Técnicas:** Ejecución en máquina local, sin GPU obligatoria
- **Tiempo:** MVP en 4-6 semanas de desarrollo
- **Presupuesto:** Solo herramientas open source y gratuitas
- **Datos:** Dataset de prueba limitado (50-100 documentos reales)

#### Dependencias
- **PaddleOCR:** Motor OCR principal (Python)
- **Tesseract:** OCR de respaldo (System)
- **LLM Local:** Llama 3 8B, Mistral 7B u similar (via Ollama)
- **Claude Code:** Entorno de desarrollo y ejecución
- **Python 3.10+:** Lenguaje principal
- **Librerías:** OpenCV, pdf2image, Pillow, pandas, numpy

---

## 2. SOFTWARE REQUIREMENTS SPECIFICATION (SRS)

### 2.1 Arquitectura del Sistema

#### 2.1.1 Vista General

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENTE LOGÍSTICO MVP                      │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
   ┌────▼────┐          ┌─────▼─────┐        ┌─────▼─────┐
   │ Entrada │          │  Pipeline │        │  Salida   │
   │         │          │   Core    │        │           │
   └────┬────┘          └─────┬─────┘        └─────▲─────┘
        │                     │                     │
        │              ┌──────┴──────┐              │
        │              │             │              │
        │         ┌────▼────┐   ┌────▼────┐         │
        │         │   OCR   │   │   LLM   │         │
        │         │ Engine  │   │ Engine  │         │
        │         └────┬────┘   └────┬────┘         │
        │              │             │              │
        │         ┌────▼─────────────▼────┐         │
        │         │   Validator Engine    │         │
        │         └───────────┬───────────┘         │
        │                     │                     │
        └─────────────────────┴─────────────────────┘

Capa de Persistencia (JSON, Logs)
```

#### 2.1.2 Componentes Principales

**1. Módulo de Entrada (Input Handler)**
- Carga de documentos (imagen/PDF)
- Conversión a formato procesable
- Validación de integridad

**2. Motor OCR (OCR Engine)**
- PaddleOCR (principal)
- Tesseract (fallback)
- Preprocesamiento de imágenes
- Detección de tablas y regiones

**3. Motor LLM (LLM Engine)**
- Conexión con modelo local (Ollama)
- Prompt engineering para extracción
- Resolución de ambigüedades
- Clasificación de documentos

**4. Motor de Validación (Validator Engine)**
- Validación cruzada
- Reglas de negocio
- Detección de inconsistencias

**5. Módulo de Salida (Output Handler)**
- Generación de JSON estructurado
- Reportes de validación
- Logs detallados

---

### 2.2 Especificaciones Técnicas Detalladas

#### 2.2.1 Stack Tecnológico

| Componente | Tecnología | Versión | Propósito |
|------------|------------|---------|-----------|
| Lenguaje | Python | 3.10+ | Desarrollo principal |
| OCR Principal | PaddleOCR | 2.7+ | Reconocimiento de texto |
| OCR Backup | Tesseract | 5.3+ | Fallback OCR |
| LLM Local | Ollama + Llama 3 | 8B | Procesamiento lenguaje |
| Preprocesamiento | OpenCV | 4.8+ | Tratamiento imágenes |
| PDF Processing | pdf2image | 1.16+ | Conversión PDF a imágenes |
| Data Structures | Pydantic | 2.5+ | Validación de datos |
| CLI Framework | Typer | 0.9+ | Interfaz línea comandos |
| Testing | pytest | 7.4+ | Testing automatizado |
| Version Control | Git | 2.40+ | Control de versiones |

---

#### 2.2.2 Estructura de Directorios

```
agente-logistica-mvp/
│
├── src/
│   ├── __init__.py
│   ├── main.py                    # Punto de entrada CLI
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── pipeline.py            # Orquestador principal
│   │   ├── config.py              # Configuración global
│   │   └── logger.py              # Sistema de logs
│   │
│   ├── input/
│   │   ├── __init__.py
│   │   ├── loader.py              # Carga de documentos
│   │   ├── preprocessor.py       # Preprocesamiento imágenes
│   │   └── validator.py           # Validación entrada
│   │
│   ├── ocr/
│   │   ├── __init__.py
│   │   ├── paddle_engine.py       # Motor PaddleOCR
│   │   ├── tesseract_engine.py    # Motor Tesseract
│   │   ├── table_detector.py      # Detección de tablas
│   │   └── region_extractor.py    # Extracción regiones
│   │
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── ollama_client.py       # Cliente Ollama
│   │   ├── prompts.py             # Templates de prompts
│   │   ├── classifier.py          # Clasificador docs
│   │   └── extractor.py           # Extractor de campos
│   │
│   ├── validator/
│   │   ├── __init__.py
│   │   ├── cross_validator.py     # Validación cruzada
│   │   ├── rules_engine.py        # Motor de reglas
│   │   └── discrepancy_detector.py # Detector discrepancias
│   │
│   ├── output/
│   │   ├── __init__.py
│   │   ├── json_exporter.py       # Exportador JSON
│   │   ├── report_generator.py    # Generador reportes
│   │   └── formatter.py           # Formateadores
│   │
│   └── models/
│       ├── __init__.py
│       ├── document.py            # Modelo de documento
│       ├── fields.py              # Modelos de campos
│       └── schemas.py             # Schemas Pydantic
│
├── templates/
│   ├── albaran.yaml               # Template albarán
│   ├── orden_envio.yaml           # Template orden envío
│   ├── nota_recepcion.yaml        # Template nota recepción
│   └── parte_transporte.yaml      # Template parte transporte
│
├── data/
│   ├── raw/                       # Documentos sin procesar
│   ├── processed/                 # Documentos procesados
│   ├── test/                      # Dataset de prueba
│   └── results/                   # Resultados y reportes
│
├── tests/
│   ├── __init__.py
│   ├── test_ocr.py
│   ├── test_llm.py
│   ├── test_validator.py
│   ├── test_integration.py
│   └── conftest.py                # Fixtures pytest
│
├── scripts/
│   ├── setup_env.sh               # Setup de entorno
│   ├── install_dependencies.sh    # Instalación dependencias
│   └── run_evaluation.py          # Script evaluación
│
├── docs/
│   ├── setup.md                   # Guía de instalación
│   ├── usage.md                   # Guía de uso
│   ├── architecture.md            # Arquitectura detallada
│   ├── api.md                     # Documentación API interna
│   └── evaluation_results.md      # Resultados evaluación
│
├── .env.example                   # Variables de entorno
├── .gitignore
├── requirements.txt               # Dependencias Python
├── pyproject.toml                 # Configuración proyecto
├── README.md                      # Documentación principal
└── LICENSE
```

---

### 2.3 Especificación de Componentes

#### 2.3.1 Módulo de Entrada (Input Handler)

**Responsabilidades:**
- Cargar documentos desde filesystem
- Validar formato y tamaño
- Convertir PDFs a imágenes
- Normalizar formato de entrada

**Clases Principales:**

```python
# src/input/loader.py

class DocumentLoader:
    """Carga documentos desde diferentes fuentes"""
    
    def load_image(self, path: str) -> np.ndarray:
        """Carga imagen desde archivo"""
        pass
    
    def load_pdf(self, path: str) -> List[np.ndarray]:
        """Carga PDF y convierte a lista de imágenes"""
        pass
    
    def validate_document(self, doc: np.ndarray) -> bool:
        """Valida integridad del documento"""
        pass

class ImagePreprocessor:
    """Preprocesa imágenes para mejorar OCR"""
    
    def denoise(self, image: np.ndarray) -> np.ndarray:
        """Reduce ruido de la imagen"""
        pass
    
    def deskew(self, image: np.ndarray) -> np.ndarray:
        """Corrige inclinación"""
        pass
    
    def enhance_contrast(self, image: np.ndarray) -> np.ndarray:
        """Mejora contraste"""
        pass
    
    def binarize(self, image: np.ndarray) -> np.ndarray:
        """Binariza imagen (blanco y negro)"""
        pass
```

**Requisitos Específicos:**

| ID | Requisito | Prioridad |
|----|-----------|-----------|
| IN-01 | Soportar formatos JPG, PNG, TIFF | CRÍTICA |
| IN-02 | Soportar PDFs multipágina | CRÍTICA |
| IN-03 | Máximo tamaño archivo: 20MB | ALTA |
| IN-04 | Resolución mínima: 150 DPI | ALTA |
| IN-05 | Validar integridad (no corruptos) | ALTA |
| IN-06 | Preprocesar automáticamente (denoise, deskew) | MEDIA |

---

#### 2.3.2 Motor OCR (OCR Engine)

**Responsabilidades:**
- Ejecutar OCR sobre imágenes preprocesadas
- Detectar tablas y estructuras
- Extraer regiones de interés
- Proporcionar texto con coordenadas

**Clases Principales:**

```python
# src/ocr/paddle_engine.py

class PaddleOCREngine:
    """Motor principal de OCR usando PaddleOCR"""
    
    def __init__(self):
        self.ocr = PaddleOCR(
            use_angle_cls=True,
            lang='es',
            use_gpu=False,  # MVP sin GPU obligatoria
            show_log=False
        )
    
    def extract_text(self, image: np.ndarray) -> List[OCRResult]:
        """Extrae texto completo con coordenadas"""
        pass
    
    def extract_table(self, image: np.ndarray) -> pd.DataFrame:
        """Extrae tabla como DataFrame"""
        pass
    
    def extract_region(self, image: np.ndarray, bbox: BBox) -> str:
        """Extrae texto de una región específica"""
        pass

# src/ocr/tesseract_engine.py

class TesseractEngine:
    """Motor de respaldo usando Tesseract"""
    
    def extract_text(self, image: np.ndarray) -> List[OCRResult]:
        """Extrae texto con Tesseract"""
        pass

# src/ocr/table_detector.py

class TableDetector:
    """Detecta y extrae tablas de documentos"""
    
    def detect_tables(self, image: np.ndarray) -> List[BBox]:
        """Detecta ubicación de tablas"""
        pass
    
    def extract_table_cells(self, image: np.ndarray, bbox: BBox) -> List[List[str]]:
        """Extrae celdas individuales de tabla"""
        pass
```

**Modelos de Datos:**

```python
# src/models/document.py

from pydantic import BaseModel
from typing import List, Tuple

class BBox(BaseModel):
    """Bounding box de región"""
    x1: int
    y1: int
    x2: int
    y2: int

class OCRResult(BaseModel):
    """Resultado de OCR por línea"""
    text: str
    bbox: BBox
    confidence: float

class TableCell(BaseModel):
    """Celda de tabla"""
    row: int
    col: int
    text: str
    bbox: BBox
```

**Requisitos Específicos:**

| ID | Requisito | Prioridad |
|----|-----------|-----------|
| OCR-01 | Accuracy >85% en texto impreso | CRÍTICA |
| OCR-02 | Soportar español (es) | CRÍTICA |
| OCR-03 | Detectar y extraer tablas | ALTA |
| OCR-04 | Proporcionar nivel de confianza por línea | ALTA |
| OCR-05 | Fallback automático a Tesseract si PaddleOCR falla | ALTA |
| OCR-06 | Reconocer sellos y firmas (detectar presencia) | MEDIA |
| OCR-07 | Procesar documento completo en <20s | ALTA |

---

#### 2.3.3 Motor LLM (LLM Engine)

**Responsabilidades:**
- Clasificar tipo de documento
- Extraer campos clave estructurados
- Resolver ambigüedades en texto OCR
- Normalizar datos extraídos

**Clases Principales:**

```python
# src/llm/ollama_client.py

class OllamaClient:
    """Cliente para interactuar con Ollama"""
    
    def __init__(self, model: str = "llama3"):
        self.model = model
        self.base_url = "http://localhost:11434"
    
    def generate(self, prompt: str, system: str = None) -> str:
        """Genera respuesta del LLM"""
        pass
    
    def generate_json(self, prompt: str, schema: dict) -> dict:
        """Genera respuesta estructurada en JSON"""
        pass

# src/llm/classifier.py

class DocumentClassifier:
    """Clasifica tipo de documento"""
    
    def __init__(self, llm_client: OllamaClient):
        self.llm = llm_client
    
    def classify(self, ocr_text: str) -> DocumentType:
        """
        Clasifica documento en una de las categorías:
        - ALBARAN
        - ORDEN_ENVIO
        - NOTA_RECEPCION
        - PARTE_TRANSPORTE
        """
        pass

# src/llm/extractor.py

class FieldExtractor:
    """Extrae campos estructurados usando LLM"""
    
    def __init__(self, llm_client: OllamaClient):
        self.llm = llm_client
    
    def extract_fields(
        self, 
        ocr_text: str, 
        doc_type: DocumentType
    ) -> Dict[str, Any]:
        """Extrae campos según template del tipo de documento"""
        pass
    
    def resolve_ambiguity(self, field: str, candidates: List[str]) -> str:
        """Resuelve ambigüedades en valores extraídos"""
        pass
```

**Templates de Prompts:**

```python
# src/llm/prompts.py

CLASSIFICATION_PROMPT = """
Analiza el siguiente texto extraído de un documento logístico y clasifica 
su tipo en una de las siguientes categorías:

1. ALBARAN: Documento de entrega de mercancías
2. ORDEN_ENVIO: Orden de despacho o envío
3. NOTA_RECEPCION: Comprobante de recepción de mercancías
4. PARTE_TRANSPORTE: Documento de transporte de mercancías

Texto del documento:
{ocr_text}

Responde SOLO con la categoría en mayúsculas (ALBARAN, ORDEN_ENVIO, 
NOTA_RECEPCION o PARTE_TRANSPORTE) y el nivel de confianza (0-100).

Formato de respuesta:
CATEGORIA: [tipo]
CONFIANZA: [0-100]
"""

EXTRACTION_PROMPT_ALBARAN = """
Extrae los siguientes campos del albarán proporcionado:

Campos obligatorios:
- numero_albaran: Número del albarán
- fecha: Fecha de emisión (formato ISO: YYYY-MM-DD)
- proveedor: Nombre del proveedor
- cliente: Nombre del cliente
- productos: Lista de productos [código, descripción, cantidad, precio_unitario]
- total: Total del albarán
- firma_presente: true/false si hay firma
- sello_presente: true/false si hay sello

Texto del documento:
{ocr_text}

Responde SOLO con un objeto JSON válido.
"""

# Similar prompts para ORDEN_ENVIO, NOTA_RECEPCION, PARTE_TRANSPORTE
```

**Requisitos Específicos:**

| ID | Requisito | Prioridad |
|----|-----------|-----------|
| LLM-01 | Clasificar con >90% accuracy | CRÍTICA |
| LLM-02 | Extraer campos con F1-score >80% | CRÍTICA |
| LLM-03 | Usar modelo local (sin conexión externa) | CRÍTICA |
| LLM-04 | Responder en <10s por documento | ALTA |
| LLM-05 | Generar salida en JSON estructurado | CRÍTICA |
| LLM-06 | Resolver ambigüedades (ej: '0' vs 'O') | ALTA |
| LLM-07 | Normalizar fechas a formato ISO | ALTA |

---

#### 2.3.4 Motor de Validación (Validator Engine)

**Responsabilidades:**
- Validar campos extraídos individualmente
- Comparar documentos relacionados
- Detectar discrepancias en cantidades, códigos, fechas
- Generar reporte de inconsistencias

**Clases Principales:**

```python
# src/validator/cross_validator.py

class CrossValidator:
    """Valida consistencia entre documentos relacionados"""
    
    def link_documents(
        self, 
        documents: List[ProcessedDocument]
    ) -> List[DocumentGroup]:
        """
        Agrupa documentos relacionados por identificadores comunes
        (ej: número de pedido, código de cliente)
        """
        pass
    
    def validate_group(self, group: DocumentGroup) -> ValidationReport:
        """Valida consistencia dentro de un grupo de documentos"""
        pass

# src/validator/rules_engine.py

class RulesEngine:
    """Motor de reglas de negocio"""
    
    def validate_quantities(
        self, 
        pedido: dict, 
        albaran: dict
    ) -> List[Discrepancy]:
        """Valida que cantidades coincidan entre pedido y albarán"""
        pass
    
    def validate_product_codes(
        self, 
        doc1: dict, 
        doc2: dict
    ) -> List[Discrepancy]:
        """Valida que códigos de productos sean consistentes"""
        pass
    
    def validate_dates(
        self, 
        pedido: dict, 
        albaran: dict
    ) -> List[Discrepancy]:
        """Valida secuencia lógica de fechas"""
        pass

# src/validator/discrepancy_detector.py

class DiscrepancyDetector:
    """Detecta tipos específicos de discrepancias"""
    
    def detect_quantity_mismatch(self, expected: int, actual: int) -> Discrepancy:
        pass
    
    def detect_missing_products(self, expected: List, actual: List) -> Discrepancy:
        pass
    
    def detect_duplicate_codes(self, products: List) -> Discrepancy:
        pass
```

**Modelos de Validación:**

```python
# src/models/schemas.py

class Discrepancy(BaseModel):
    """Representa una discrepancia detectada"""
    type: str  # 'quantity_mismatch', 'missing_product', etc.
    severity: str  # 'critical', 'warning', 'info'
    field: str
    expected: Any
    actual: Any
    description: str
    suggested_action: str

class ValidationReport(BaseModel):
    """Reporte de validación completo"""
    document_group_id: str
    total_documents: int
    discrepancies: List[Discrepancy]
    status: str  # 'valid', 'warning', 'invalid'
    timestamp: datetime
    summary: str
```

**Requisitos Específicos:**

| ID | Requisito | Prioridad |
|----|-----------|-----------|
| VAL-01 | Detectar discrepancias de cantidad (±10%) | CRÍTICA |
| VAL-02 | Detectar códigos de producto erróneos | ALTA |
| VAL-03 | Validar secuencia lógica de fechas | ALTA |
| VAL-04 | Detectar productos duplicados | MEDIA |
| VAL-05 | Generar reporte con severidad (critical/warning/info) | ALTA |
| VAL-06 | Sugerir acciones correctivas | MEDIA |
| VAL-07 | Recall >75% en detección de errores | ALTA |

---

#### 2.3.5 Pipeline Principal (Core Pipeline)

**Responsabilidades:**
- Orquestar flujo completo de procesamiento
- Manejar errores y reintentos
- Gestionar logging
- Coordinar componentes

**Clase Principal:**

```python
# src/core/pipeline.py

class DocumentProcessingPipeline:
    """Pipeline principal de procesamiento"""
    
    def __init__(self, config: Config):
        self.config = config
        self.loader = DocumentLoader()
        self.preprocessor = ImagePreprocessor()
        self.ocr_engine = PaddleOCREngine()
        self.ocr_fallback = TesseractEngine()
        self.llm_client = OllamaClient()
        self.classifier = DocumentClassifier(self.llm_client)
        self.extractor = FieldExtractor(self.llm_client)
        self.validator = CrossValidator()
        self.logger = setup_logger()
    
    def process_document(self, file_path: str) -> ProcessedDocument:
        """
        Procesa un documento completo end-to-end
        
        Flujo:
        1. Cargar documento
        2. Preprocesar imagen
        3. Ejecutar OCR
        4. Clasificar documento
        5. Extraer campos
        6. Validar datos
        7. Generar salida
        """
        try:
            # 1. Carga
            self.logger.info(f"Cargando documento: {file_path}")
            image = self.loader.load_image(file_path)
            
            # 2. Preprocesamiento
            self.logger.info("Preprocesando imagen")
            processed_image = self.preprocessor.denoise(image)
            processed_image = self.preprocessor.deskew(processed_image)
            processed_image = self.preprocessor.enhance_contrast(processed_image)
            
            # 3. OCR
            self.logger.info("Ejecutando OCR")
            try:
                ocr_results = self.ocr_engine.extract_text(processed_image)
            except Exception as e:
                self.logger.warning(f"PaddleOCR falló, usando Tesseract: {e}")
                ocr_results = self.ocr_fallback.extract_text(processed_image)
            
            ocr_text = " ".join([r.text for r in ocr_results])
            
            # 4. Clasificación
            self.logger.info("Clasificando documento")
            doc_type = self.classifier.classify(ocr_text)
            
            # 5. Extracción
            self.logger.info(f"Extrayendo campos para tipo: {doc_type}")
            extracted_fields = self.extractor.extract_fields(ocr_text, doc_type)
            
            # 6. Validación individual
            self.logger.info("Validando campos")
            validation_result = self.validate_fields(extracted_fields)
            
            # 7. Generar resultado
            result = ProcessedDocument(
                file_path=file_path,
                document_type=doc_type,
                ocr_confidence=self._calculate_avg_confidence(ocr_results),
                extracted_fields=extracted_fields,
                validation=validation_result,
                timestamp=datetime.now()
            )
            
            self.logger.info("Documento procesado exitosamente")
            return result
            
        except Exception as e:
            self.logger.error(f"Error procesando documento: {e}")
            raise
    
    def process_batch(self, file_paths: List[str]) -> List[ProcessedDocument]:
        """Procesa un lote de documentos"""
        pass
    
    def validate_cross_documents(
        self, 
        documents: List[ProcessedDocument]
    ) -> ValidationReport:
        """Valida cruce de documentos relacionados"""
        pass
```

---

### 2.4 Campos Clave por Tipo de Documento

#### 2.4.1 Albarán de Entrega

```yaml
# templates/albaran.yaml

nombre: Albarán de Entrega
descripcion: Documento que acredita la entrega de mercancías

campos_obligatorios:
  - numero_albaran:
      tipo: string
      patron: "^ALB-\d{8}$"
      ejemplo: "ALB-20250115"
  
  - fecha_emision:
      tipo: date
      formato: "YYYY-MM-DD"
      validacion: "no_futuro"
  
  - proveedor:
      tipo: string
      subcampos:
        - razon_social
        - cif
        - direccion
  
  - cliente:
      tipo: string
      subcampos:
        - razon_social
        - cif
        - direccion_entrega
  
  - productos:
      tipo: array
      min_items: 1
      schema:
        - codigo_producto: string
        - descripcion: string
        - cantidad: integer
        - precio_unitario: float
        - subtotal: float
  
  - total:
      tipo: float
      validacion: "suma_subtotales"
  
  - firma_transportista:
      tipo: boolean
      descripcion: "Indica si hay firma"
  
  - sello_empresa:
      tipo: boolean
      descripcion: "Indica si hay sello"
  
  - observaciones:
      tipo: string
      opcional: true

regiones_documento:
  - cabecera: [0, 0, 1000, 200]
  - tabla_productos: [0, 200, 1000, 800]
  - pie: [0, 800, 1000, 1000]
```

#### 2.4.2 Orden de Envío

```yaml
# templates/orden_envio.yaml

nombre: Orden de Envío
descripcion: Instrucción de despacho de mercancías

campos_obligatorios:
  - numero_orden:
      tipo: string
      patron: "^ORD-\d{8}$"
  
  - fecha_orden:
      tipo: date
      formato: "YYYY-MM-DD"
  
  - fecha_envio_programada:
      tipo: date
      formato: "YYYY-MM-DD"
      validacion: "posterior_a_fecha_orden"
  
  - origen:
      tipo: string
      subcampos:
        - almacen
        - direccion
        - codigo_postal
  
  - destino:
      tipo: string
      subcampos:
        - cliente
        - direccion_entrega
        - codigo_postal
  
  - productos:
      tipo: array
      schema:
        - codigo: string
        - descripcion: string
        - cantidad_ordenada: integer
        - ubicacion_almacen: string
  
  - transportista:
      tipo: string
      opcional: true
  
  - instrucciones_especiales:
      tipo: string
      opcional: true
```

#### 2.4.3 Nota de Recepción

```yaml
# templates/nota_recepcion.yaml

nombre: Nota de Recepción
descripcion: Comprobante de recepción de mercancías

campos_obligatorios:
  - numero_recepcion:
      tipo: string
      patron: "^REC-\d{8}$"
  
  - fecha_recepcion:
      tipo: date
      formato: "YYYY-MM-DD"
  
  - referencia_pedido:
      tipo: string
      descripcion: "Número de pedido original"
  
  - referencia_albaran:
      tipo: string
      descripcion: "Número de albarán asociado"
      validacion: "debe_existir_albaran"
  
  - proveedor:
      tipo: string
  
  - productos_recibidos:
      tipo: array
      schema:
        - codigo: string
        - descripcion: string
        - cantidad_esperada: integer
        - cantidad_recibida: integer
        - estado: enum [correcto, dañado, faltante]
        - observaciones: string
  
  - discrepancias:
      tipo: boolean
      descripcion: "true si hay diferencias entre esperado y recibido"
  
  - firma_receptor:
      tipo: boolean
  
  - observaciones_calidad:
      tipo: string
      opcional: true
```

#### 2.4.4 Parte de Transporte

```yaml
# templates/parte_transporte.yaml

nombre: Parte de Transporte
descripcion: Documento de control de transporte de mercancías

campos_obligatorios:
  - numero_parte:
      tipo: string
      patron: "^PT-\d{8}$"
  
  - fecha_salida:
      tipo: datetime
      formato: "YYYY-MM-DD HH:MM"
  
  - fecha_llegada_estimada:
      tipo: datetime
      formato: "YYYY-MM-DD HH:MM"
  
  - matricula_vehiculo:
      tipo: string
      patron: "^\d{4}-[A-Z]{3}$"
      ejemplo: "1234-ABC"
  
  - conductor:
      tipo: string
      subcampos:
        - nombre: string
        - dni: string
        - licencia: string
  
  - origen:
      tipo: string
      subcampos:
        - ubicacion: string
        - codigo_postal: string
  
  - destino:
      tipo: string
      subcampos:
        - ubicacion: string
        - codigo_postal: string
  
  - carga:
      tipo: array
      schema:
        - numero_albaran: string
        - bultos: integer
        - peso_kg: float
  
  - kilometraje_inicial:
      tipo: integer
  
  - kilometraje_final:
      tipo: integer
      opcional: true
  
  - firma_origen:
      tipo: boolean
  
  - firma_destino:
      tipo: boolean
      opcional: true
  
  - incidencias:
      tipo: string
      opcional: true
```

---

### 2.5 Flujo de Datos Detallado

#### 2.5.1 Procesamiento de un Solo Documento

```
┌─────────────────┐
│  Usuario CLI    │
│  $ python main  │
│  --file doc.pdf │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  1. DocumentLoader                      │
│  - Cargar archivo                       │
│  - Validar formato                      │
│  - Convertir PDF → imágenes (si aplica) │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  2. ImagePreprocessor                   │
│  - Denoise                              │
│  - Deskew                               │
│  - Enhance contrast                     │
│  - Binarize (opcional)                  │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  3. OCR Engine (PaddleOCR)              │
│  - Detectar texto completo              │
│  - Extraer con coordenadas              │
│  - Calcular confianza                   │
│  - Si falla → Tesseract                 │
└────────┬────────────────────────────────┘
         │
         ├──────────────────┐
         │                  │
         ▼                  ▼
┌─────────────────┐  ┌─────────────────┐
│ TableDetector   │  │ RegionExtractor │
│ - Detectar      │  │ - Cabecera      │
│   tablas        │  │ - Pie           │
│ - Extraer       │  │ - Sellos        │
│   celdas        │  │ - Firmas        │
└────────┬────────┘  └────────┬────────┘
         │                    │
         └──────────┬─────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│  4. DocumentClassifier (LLM)            │
│  - Analizar texto OCR                   │
│  - Clasificar tipo documento            │
│  - Retornar: ALBARAN | ORDEN_ENVIO |    │
│    NOTA_RECEPCION | PARTE_TRANSPORTE    │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  5. FieldExtractor (LLM)                │
│  - Cargar template según tipo           │
│  - Extraer campos estructurados         │
│  - Resolver ambigüedades                │
│  - Normalizar valores                   │
│  - Generar JSON                         │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  6. Field Validator                     │
│  - Validar tipos de datos               │
│  - Validar patrones (regex)             │
│  - Validar rangos                       │
│  - Validar suma de totales              │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  7. JSON Exporter                       │
│  - Formatear resultado                  │
│  - Guardar en /data/processed/          │
│  - Generar log de procesamiento         │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  Resultado JSON │
│  + Reporte Log  │
└─────────────────┘
```

#### 2.5.2 Validación Cruzada de Documentos

```
┌─────────────────────────────────────────┐
│  Usuario CLI                            │
│  $ python main --validate-group         │
│    doc1.json doc2.json doc3.json        │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  1. CrossValidator                      │
│  - Cargar documentos procesados (JSON)  │
│  - Identificar relaciones               │
│    (mismos números de pedido, etc.)     │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  2. DocumentGrouper                     │
│  - Agrupar por:                         │
│    * Número de pedido                   │
│    * Cliente                            │
│    * Fecha cercana                      │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  3. RulesEngine (por cada grupo)        │
│  - Validar cantidades                   │
│    PEDIDO.cantidad == ALBARAN.cantidad  │
│  - Validar códigos de producto          │
│  - Validar secuencia de fechas          │
│    fecha_pedido < fecha_envio <         │
│    fecha_recepcion                      │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  4. DiscrepancyDetector                 │
│  - Identificar tipo de discrepancia     │
│  - Calcular severidad                   │
│  - Generar descripción                  │
│  - Sugerir acción correctiva            │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  5. ReportGenerator                     │
│  - Crear ValidationReport               │
│  - Listar discrepancias por severidad   │
│  - Incluir resumen ejecutivo            │
│  - Exportar JSON + PDF (futuro)         │
└────────┬────────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  Reporte Final  │
│  JSON + Logs    │
└─────────────────┘
```

---

### 2.6 Interfaz CLI (Command Line Interface)

#### 2.6.1 Comandos Principales

```bash
# Comando principal
python src/main.py [COMMAND] [OPTIONS]

# Comandos disponibles:

# 1. Procesar un documento individual
python src/main.py process \
  --file data/raw/albaran_001.pdf \
  --output data/processed/albaran_001.json \
  --verbose

# 2. Procesar lote de documentos
python src/main.py batch \
  --input-dir data/raw/ \
  --output-dir data/processed/ \
  --workers 4

# 3. Validar cruce de documentos
python src/main.py validate \
  --group data/processed/grupo_pedido_12345/*.json \
  --report data/results/validation_report.json

# 4. Evaluar precisión (con ground truth)
python src/main.py evaluate \
  --test-dir data/test/ \
  --ground-truth data/test/ground_truth.json \
  --metrics-output data/results/metrics.json

# 5. Ver configuración actual
python src/main.py config --show

# 6. Configurar motor OCR
python src/main.py config --ocr-engine paddle  # o tesseract

# 7. Configurar modelo LLM
python src/main.py config --llm-model llama3:8b

# 8. Modo interactivo (para debugging)
python src/main.py interactive
```

#### 2.6.2 Opciones Globales

```bash
--verbose, -v         # Modo verbose (más logs)
--quiet, -q          # Modo silencioso
--log-file PATH      # Guardar logs en archivo
--config PATH        # Usar archivo de configuración custom
--no-gpu             # Forzar ejecución sin GPU
--help, -h           # Ayuda
--version            # Versión del agente
```

#### 2.6.3 Ejemplo de Salida CLI

```bash
$ python src/main.py process --file data/raw/albaran_001.pdf --verbose

[2025-12-17 14:30:00] INFO: Iniciando procesamiento de documento
[2025-12-17 14:30:00] INFO: Cargando documento: albaran_001.pdf
[2025-12-17 14:30:01] INFO: Preprocesando imagen (denoise, deskew, contrast)
[2025-12-17 14:30:03] INFO: Ejecutando OCR con PaddleOCR
[2025-12-17 14:30:15] INFO: OCR completado - Confianza promedio: 92.5%
[2025-12-17 14:30:15] INFO: Clasificando documento con LLM
[2025-12-17 14:30:18] INFO: Documento clasificado como: ALBARAN (confianza: 95%)
[2025-12-17 14:30:18] INFO: Extrayendo campos estructurados
[2025-12-17 14:30:25] INFO: Campos extraídos: 12/12 campos obligatorios
[2025-12-17 14:30:25] INFO: Validando campos individuales
[2025-12-17 14:30:26] INFO: Validación OK - 0 errores, 1 warning
[2025-12-17 14:30:26] WARNING: Campo 'observaciones' vacío (opcional)
[2025-12-17 14:30:26] INFO: Guardando resultado en: data/processed/albaran_001.json
[2025-12-17 14:30:26] SUCCESS: Documento procesado exitosamente

Resumen:
--------
Documento: albaran_001.pdf
Tipo: ALBARAN
Confianza OCR: 92.5%
Confianza Clasificación: 95%
Campos extraídos: 12/12
Tiempo total: 26.3s

Ver resultado completo en: data/processed/albaran_001.json
```

---

### 2.7 Formato de Salida JSON

#### 2.7.1 Documento Procesado

```json
{
  "metadata": {
    "file_path": "data/raw/albaran_001.pdf",
    "file_name": "albaran_001.pdf",
    "file_size_kb": 245,
    "processing_timestamp": "2025-12-17T14:30:26Z",
    "processing_time_seconds": 26.3,
    "agent_version": "1.0.0"
  },
  "classification": {
    "document_type": "ALBARAN",
    "confidence": 0.95,
    "alternative_types": []
  },
  "ocr_info": {
    "engine_used": "PaddleOCR",
    "average_confidence": 0.925,
    "total_text_blocks": 47,
    "tables_detected": 1,
    "signatures_detected": true,
    "stamps_detected": true
  },
  "extracted_fields": {
    "numero_albaran": "ALB-20250115",
    "fecha_emision": "2025-01-15",
    "proveedor": {
      "razon_social": "Distribuciones López S.L.",
      "cif": "B12345678",
      "direccion": "Calle Mayor 123, Madrid"
    },
    "cliente": {
      "razon_social": "Farmacia García",
      "cif": "B87654321",
      "direccion_entrega": "Avenida Principal 45, Barcelona"
    },
    "productos": [
      {
        "codigo_producto": "MED-001",
        "descripcion": "Paracetamol 500mg x100",
        "cantidad": 50,
        "precio_unitario": 4.50,
        "subtotal": 225.00
      },
      {
        "codigo_producto": "MED-002",
        "descripcion": "Ibuprofeno 600mg x50",
        "cantidad": 30,
        "precio_unitario": 6.80,
        "subtotal": 204.00
      }
    ],
    "total": 429.00,
    "firma_transportista": true,
    "sello_empresa": true,
    "observaciones": ""
  },
  "validation": {
    "status": "valid",
    "errors": [],
    "warnings": [
      {
        "field": "observaciones",
        "message": "Campo opcional vacío",
        "severity": "info"
      }
    ]
  },
  "raw_ocr_text": "ALBARAN DE ENTREGA\nNúmero: ALB-20250115\n...[texto completo]"
}
```

#### 2.7.2 Reporte de Validación Cruzada

```json
{
  "validation_report": {
    "report_id": "VAL-20250117-001",
    "timestamp": "2025-12-17T15:00:00Z",
    "document_group": {
      "group_id": "PEDIDO-12345",
      "total_documents": 3,
      "documents": [
        {
          "file": "orden_envio_12345.json",
          "type": "ORDEN_ENVIO"
        },
        {
          "file": "albaran_001.json",
          "type": "ALBARAN"
        },
        {
          "file": "nota_recepcion_001.json",
          "type": "NOTA_RECEPCION"
        }
      ]
    },
    "status": "warnings",
    "discrepancies": [
      {
        "discrepancy_id": "DISC-001",
        "type": "quantity_mismatch",
        "severity": "warning",
        "affected_documents": [
          "orden_envio_12345.json",
          "albaran_001.json"
        ],
        "field": "productos[0].cantidad",
        "expected": {
          "document": "orden_envio_12345.json",
          "value": 50
        },
        "actual": {
          "document": "albaran_001.json",
          "value": 48
        },
        "difference": -2,
        "difference_percentage": -4.0,
        "description": "Cantidad en albarán menor que en orden de envío para producto MED-001",
        "suggested_action": "Verificar si faltaron 2 unidades en el envío o si es error de transcripción",
        "business_rule_violated": "orden_cantidad == albaran_cantidad"
      },
      {
        "discrepancy_id": "DISC-002",
        "type": "date_sequence_invalid",
        "severity": "critical",
        "affected_documents": [
          "albaran_001.json",
          "nota_recepcion_001.json"
        ],
        "field": "fecha",
        "dates": {
          "fecha_envio": "2025-01-15",
          "fecha_recepcion": "2025-01-14"
        },
        "description": "Fecha de recepción anterior a fecha de envío",
        "suggested_action": "Revisar y corregir fecha de recepción (probable error de entrada)",
        "business_rule_violated": "fecha_recepcion >= fecha_envio"
      }
    ],
    "summary": {
      "total_discrepancies": 2,
      "critical": 1,
      "warnings": 1,
      "info": 0,
      "overall_status": "requires_review"
    },
    "recommendations": [
      "Revisar manualmente los 2 productos con discrepancias de cantidad",
      "Corregir fecha de recepción en el sistema"
    ]
  }
}
```

---

### 2.8 Plan de Evaluación y Métricas

#### 2.8.1 Dataset de Prueba

**Composición:**
- 50 documentos reales anonimizados
- Distribución:
  - 15 Albaranes
  - 12 Órdenes de Envío
  - 13 Notas de Recepción
  - 10 Partes de Transporte

**Ground Truth:**
- Cada documento con anotación manual de:
  - Tipo de documento correcto
  - Campos clave extraídos manualmente
  - Validaciones esperadas

**Características del dataset:**
- Variedad de calidades de imagen (excelente, buena, regular)
- Variedad de formatos (escaneados, fotografías, PDFs nativos)
- Documentos con tablas complejas
- Documentos con sellos y firmas
- Documentos con anotaciones manuscritas (para medir limitaciones)

#### 2.8.2 Métricas a Evaluar

**1. Precisión OCR**

```python
def evaluate_ocr_accuracy(predicted_text: str, ground_truth: str) -> float:
    """
    Calcula Character Error Rate (CER) y Word Error Rate (WER)
    """
    cer = character_error_rate(predicted_text, ground_truth)
    wer = word_error_rate(predicted_text, ground_truth)
    
    accuracy = 1 - cer
    return accuracy

# Objetivo: >85% accuracy
```

**2. Precisión de Clasificación**

```python
def evaluate_classification(predictions: List, ground_truth: List) -> dict:
    """
    Calcula accuracy, precision, recall, F1 por clase
    """
    accuracy = accuracy_score(ground_truth, predictions)
    precision = precision_score(ground_truth, predictions, average='macro')
    recall = recall_score(ground_truth, predictions, average='macro')
    f1 = f1_score(ground_truth, predictions, average='macro')
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1
    }

# Objetivo: >90% accuracy
```

**3. F1-Score de Extracción por Campo**

```python
def evaluate_field_extraction(predicted_fields: dict, ground_truth: dict) -> dict:
    """
    Calcula F1-score por campo individual
    """
    results = {}
    
    for field_name in ground_truth.keys():
        predicted = predicted_fields.get(field_name)
        expected = ground_truth[field_name]
        
        # Exact match
        exact_match = (predicted == expected)
        
        # Fuzzy match (para strings)
        if isinstance(expected, str):
            similarity = fuzz.ratio(predicted, expected) / 100
        else:
            similarity = 1.0 if exact_match else 0.0
        
        results[field_name] = {
            'exact_match': exact_match,
            'similarity': similarity
        }
    
    avg_similarity = np.mean([r['similarity'] for r in results.values()])
    
    return {
        'per_field': results,
        'average_similarity': avg_similarity
    }

# Objetivo: >80% F1-score promedio
```

**4. Recall en Detección de Discrepancias**

```python
def evaluate_discrepancy_detection(
    predicted_discrepancies: List[Discrepancy],
    ground_truth_discrepancies: List[Discrepancy]
) -> dict:
    """
    Mide capacidad de detectar discrepancias reales
    """
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    
    # Comparar discrepancias detectadas vs reales
    for gt_disc in ground_truth_discrepancies:
        found = any(
            pred_disc.type == gt_disc.type and
            pred_disc.field == gt_disc.field
            for pred_disc in predicted_discrepancies
        )
        if found:
            true_positives += 1
        else:
            false_negatives += 1
    
    for pred_disc in predicted_discrepancies:
        is_real = any(
            gt_disc.type == pred_disc.type and
            gt_disc.field == pred_disc.field
            for gt_disc in ground_truth_discrepancies
        )
        if not is_real:
            false_positives += 1
    
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'true_positives': true_positives,
        'false_positives': false_positives,
        'false_negatives': false_negatives
    }

# Objetivo: >75% recall
```

**5. Tiempo de Procesamiento**

```python
def evaluate_performance(processing_times: List[float]) -> dict:
    """
    Analiza tiempos de procesamiento
    """
    return {
        'mean': np.mean(processing_times),
        'median': np.median(processing_times),
        'std': np.std(processing_times),
        'min': np.min(processing_times),
        'max': np.max(processing_times),
        'p95': np.percentile(processing_times, 95)
    }

# Objetivo: <30s/documento (media)
```

#### 2.8.3 Script de Evaluación

```python
# scripts/run_evaluation.py

def run_full_evaluation():
    """
    Ejecuta evaluación completa del sistema
    """
    
    # 1. Cargar dataset de prueba
    test_docs = load_test_dataset('data/test/')
    ground_truth = load_ground_truth('data/test/ground_truth.json')
    
    # 2. Procesar todos los documentos
    results = []
    processing_times = []
    
    for doc in test_docs:
        start_time = time.time()
        result = pipeline.process_document(doc.path)
        elapsed = time.time() - start_time
        
        results.append(result)
        processing_times.append(elapsed)
    
    # 3. Evaluar OCR
    ocr_metrics = evaluate_ocr_accuracy_batch(results, ground_truth)
    
    # 4. Evaluar Clasificación
    classification_metrics = evaluate_classification(
        [r.document_type for r in results],
        [gt.document_type for gt in ground_truth]
    )
    
    # 5. Evaluar Extracción de Campos
    extraction_metrics = evaluate_field_extraction_batch(results, ground_truth)
    
    # 6. Evaluar Validación Cruzada
    validation_metrics = evaluate_discrepancy_detection_batch(results, ground_truth)
    
    # 7. Evaluar Performance
    performance_metrics = evaluate_performance(processing_times)
    
    # 8. Generar reporte completo
    report = {
        'evaluation_date': datetime.now().isoformat(),
        'dataset_size': len(test_docs),
        'ocr': ocr_metrics,
        'classification': classification_metrics,
        'extraction': extraction_metrics,
        'validation': validation_metrics,
        'performance': performance_metrics,
        'meets_objectives': {
            'ocr_accuracy': ocr_metrics['accuracy'] > 0.85,
            'classification_accuracy': classification_metrics['accuracy'] > 0.90,
            'extraction_f1': extraction_metrics['average_f1'] > 0.80,
            'validation_recall': validation_metrics['recall'] > 0.75,
            'processing_time': performance_metrics['mean'] < 30.0
        }
    }
    
    # 9. Guardar reporte
    save_evaluation_report(report, 'data/results/evaluation_report.json')
    
    # 10. Generar visualizaciones
    generate_evaluation_plots(report, 'data/results/plots/')
    
    return report
```

---

### 2.9 Configuración del Sistema

#### 2.9.1 Archivo de Configuración

```yaml
# config.yaml

# Configuración General
general:
  version: "1.0.0"
  log_level: "INFO"  # DEBUG, INFO, WARNING, ERROR
  log_file: "logs/agente.log"
  data_dir: "data/"
  temp_dir: "/tmp/agente-logistica"

# Configuración de Entrada
input:
  supported_formats: ["jpg", "jpeg", "png", "tiff", "pdf"]
  max_file_size_mb: 20
  min_resolution_dpi: 150

# Configuración de Preprocesamiento
preprocessing:
  denoise: true
  denoise_strength: 3
  deskew: true
  deskew_threshold: 0.5
  enhance_contrast: true
  contrast_method: "clahe"  # clahe, histogram
  binarize: false

# Configuración OCR
ocr:
  primary_engine: "paddleocr"  # paddleocr, tesseract
  fallback_engine: "tesseract"
  language: "es"
  use_gpu: false
  confidence_threshold: 0.7
  
  paddleocr:
    use_angle_cls: true
    det_db_thresh: 0.3
    det_db_box_thresh: 0.6
    det_db_unclip_ratio: 1.5
  
  tesseract:
    psm: 3  # Page segmentation mode
    oem: 3  # OCR Engine Mode

# Configuración LLM
llm:
  provider: "ollama"
  model: "llama3:8b"
  base_url: "http://localhost:11434"
  timeout_seconds: 30
  max_retries: 3
  temperature: 0.1  # Bajo para consistencia
  
  classification:
    max_tokens: 100
    confidence_threshold: 0.8
  
  extraction:
    max_tokens: 2000
    use_json_mode: true

# Configuración de Validación
validation:
  quantity_tolerance_percent: 10
  date_sequence_strict: true
  require_all_mandatory_fields: true
  
  cross_validation:
    enable: true
    link_by: ["numero_pedido", "cliente"]
    max_date_diff_days: 30

# Configuración de Salida
output:
  format: "json"
  pretty_print: true
  include_raw_ocr: true
  include_metadata: true
  output_dir: "data/processed/"

# Configuración de Performance
performance:
  max_workers: 4
  processing_timeout_seconds: 60
  enable_caching: true
  cache_dir: "cache/"

# Configuración de Evaluación
evaluation:
  test_data_dir: "data/test/"
  ground_truth_file: "data/test/ground_truth.json"
  results_dir: "data/results/"
  generate_plots: true
```

#### 2.9.2 Variables de Entorno

```bash
# .env.example

# Directorios
DATA_DIR=data/
LOG_DIR=logs/
TEMP_DIR=/tmp/agente-logistica

# OCR
TESSDATA_PREFIX=/usr/share/tesseract-ocr/5/tessdata/
PADDLE_GPU=0

# LLM
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3:8b

# Configuración
CONFIG_FILE=config.yaml
LOG_LEVEL=INFO

# Performance
MAX_WORKERS=4
ENABLE_GPU=false
```

---

### 2.10 Instalación y Configuración del Entorno

#### 2.10.1 Requisitos del Sistema

**Requisitos Mínimos:**
- **OS:** Windows 10+, macOS 11+, Ubuntu 20.04+
- **Python:** 3.10+
- **RAM:** 8GB (16GB recomendado)
- **Almacenamiento:** 5GB libres
- **CPU:** 4 cores (8 recomendado)
- **GPU:** Opcional (acelera OCR y LLM)

**Software Requerido:**
- Python 3.10+
- Tesseract OCR 5.3+
- Ollama (para LLM local)
- Git
- Visual Studio Code
- Claude Code Extension

#### 2.10.2 Guía de Instalación

```bash
# 1. Clonar repositorio
git clone https://github.com/tu-org/agente-logistica-mvp.git
cd agente-logistica-mvp

# 2. Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias Python
pip install --upgrade pip
pip install -r requirements.txt

# 4. Instalar Tesseract
# Ubuntu/Debian:
sudo apt-get install tesseract-ocr tesseract-ocr-spa

# macOS:
brew install tesseract tesseract-lang

# Windows:
# Descargar instalador desde: https://github.com/UB-Mannheim/tesseract/wiki
# Añadir al PATH

# 5. Instalar Ollama
# Descargar desde: https://ollama.ai
# O con script:
curl -fsSL https://ollama.com/install.sh | sh

# 6. Descargar modelo LLM
ollama pull llama3:8b

# 7. Verificar instalación
python scripts/verify_installation.py

# 8. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus rutas

# 9. Ejecutar tests
pytest tests/ -v

# 10. Probar con documento de ejemplo
python src/main.py process \
  --file data/examples/albaran_ejemplo.pdf \
  --output data/processed/test.json \
  --verbose
```

#### 2.10.3 Configuración en VS Code con Claude Code

```bash
# 1. Instalar extensión Claude Code en VS Code
# Desde marketplace: Claude Code

# 2. Configurar Claude Code
# Crear archivo .claude/config.json en el proyecto:
{
  "model": "claude-sonnet-4",
  "project_root": ".",
  "context_files": [
    "README.md",
    "docs/architecture.md",
    "src/**/*.py"
  ],
  "ignore_patterns": [
    "venv/",
    "__pycache__/",
    "*.pyc",
    "data/raw/*"
  ]
}

# 3. Abrir proyecto en VS Code
code .

# 4. Activar entorno virtual en terminal integrada
source venv/bin/activate

# 5. Ejecutar agente desde terminal VS Code
python src/main.py --help
```

---

### 2.11 Limitaciones Conocidas y Trabajo Futuro

#### 2.11.1 Limitaciones del MVP

**Limitaciones Técnicas:**

1. **OCR:**
   - Escritura manual no soportada (solo texto impreso)
   - Calidad de imagen baja (<150 DPI) afecta precisión
   - Documentos muy deteriorados pueden fallar
   - Idiomas diferentes a español no soportados

2. **LLM:**
   - Modelos locales tienen menor capacidad que GPT-4
   - Ambigüedades complejas pueden no resolverse
   - Requiere prompts bien diseñados por tipo de documento
   - Lento sin GPU (>10s por documento)

3. **Validación:**
   - Solo valida reglas básicas (cantidades, fechas, códigos)
   - No detecta fraude sofisticado
   - Requiere documentos relacionados para validación cruzada

4. **Escalabilidad:**
   - Diseñado para <100 docs/día
   - Sin procesamiento paralelo avanzado
   - Sin sistema de colas

5. **Integración:**
   - Sin API REST
   - Sin integración directa con ERP/WMS
   - Salida solo en JSON (no XML, EDI, etc.)

**Limitaciones de Alcance:**

- No incluye interfaz gráfica
- No incluye sistema de aprendizaje continuo
- No incluye detección de fraude avanzada
- No incluye multi-idioma
- No incluye reconocimiento de firmas biométricas

#### 2.11.2 Trabajo Futuro (Post-MVP)

**Fase 2 - Mejoras Técnicas (3-6 meses):**

1. **OCR Avanzado:**
   - Soporte para escritura manual (PaddleOCR + modelo custom)
   - Multi-idioma (inglés, portugués)
   - Mejora de preprocesamiento con ML

2. **LLM:**
   - Fine-tuning de modelo específico para documentos logísticos
   - Sistema de embeddings para búsqueda semántica
   - Chain-of-thought prompting para razonamiento complejo

3. **Validación:**
   - Motor de reglas avanzado (más reglas de negocio)
   - Detección de anomalías con ML
   - Validación con bases de datos externas

**Fase 3 - Integración y Escalabilidad (6-12 meses):**

1. **API REST:**
   - Endpoint para procesamiento asíncrono
   - Webhooks para notificaciones
   - Autenticación y autorización

2. **Integración ERP/WMS:**
   - Conectores para SAP, Oracle, Microsoft Dynamics
   - Plugins para WMS populares (Manhattan, HighJump)
   - Soporte para EDI (EDIFACT, ANSI X12)

3. **Escalabilidad:**
   - Arquitectura de microservicios
   - Procesamiento batch masivo (>1000 docs/día)
   - Sistema de colas (RabbitMQ, Kafka)
   - Distribución de carga

4. **Interfaz:**
   - Web UI para gestión y supervisión
   - Dashboard de métricas en tiempo real
   - Sistema de aprobación manual de documentos

**Fase 4 - Inteligencia Avanzada (12-18 meses):**

1. **Aprendizaje Continuo:**
   - Retraining automático con feedback
   - Active learning para casos difíciles
   - Mejora continua de precisión

2. **Detección de Fraude:**
   - Análisis de patrones sospechosos
   - Detección de manipulación de documentos
   - Verificación de autenticidad de sellos y firmas

3. **Analytics:**
   - Reportes de tendencias y KPIs logísticos
   - Predicción de discrepancias
   - Optimización de procesos

---

### 2.12 Diseño de Integración con ERP/WMS (Propuesta Futura)

#### 2.12.1 Arquitectura de Integración Propuesta

```
┌─────────────────────────────────────────────────────────────┐
│                    AGENTE LOGÍSTICO                          │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   OCR        │  │     LLM      │  │  Validator   │      │
│  │   Engine     │  │   Engine     │  │   Engine     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │             API REST (FastAPI)                     │     │
│  │  POST /api/v1/documents/process                    │     │
│  │  POST /api/v1/documents/validate                   │     │
│  │  GET  /api/v1/documents/{id}                       │     │
│  └────────────────────────────────────────────────────┘     │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          │ REST API / Webhooks
                          │
         ┌────────────────┼────────────────┐
         │                │                │
         ▼                ▼                ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   SAP ERP    │  │  Oracle WMS  │  │  Custom ERP  │
│              │  │              │  │              │
│  - Pedidos   │  │  - Recepciones│  │  - Albaranes │
│  - Facturas  │  │  - Envíos    │  │  - Inventario│
└──────────────┘  └──────────────┘  └──────────────┘
```

#### 2.12.2 Conectores Propuestos

**Conector SAP:**
```python
class SAPConnector:
    """Conector para SAP ECC/S4HANA"""
    
    def push_albaran(self, albaran_data: dict) -> str:
        """Crea documento de entrega (LIKP/LIPS)"""
        pass
    
    def validate_pedido(self, numero_pedido: str) -> dict:
        """Valida contra pedido en SAP (VBAK/VBAP)"""
        pass
```

**Conector WMS Genérico:**
```python
class WMSConnector:
    """Conector genérico para WMS"""
    
    def create_receipt(self, receipt_data: dict) -> str:
        """Crea recepción en WMS"""
        pass
    
    def update_inventory(self, movements: List[dict]) -> bool:
        """Actualiza inventario"""
        pass
```

---

## 3. PLAN DE IMPLEMENTACIÓN

### 3.1 Cronograma Estimado

| Fase | Duración | Entregables |
|------|----------|-------------|
| **Sprint 1:** Setup y OCR | 1 semana | Estructura proyecto, OCR básico funcionando |
| **Sprint 2:** LLM y Clasificación | 1 semana | Clasificación de documentos, templates |
| **Sprint 3:** Extracción de Campos | 1 semana | Extracción estructurada, validación individual |
| **Sprint 4:** Validación Cruzada | 1 semana | Validación cruzada, detección discrepancias |
| **Sprint 5:** CLI y Testing | 1 semana | Interfaz CLI completa, tests automatizados |
| **Sprint 6:** Evaluación y Documentación | 1 semana | Métricas, evaluación, documentación final |

**Total:** 6 semanas

### 3.2 Entregables Finales

1. **Código Fuente:**
   - Repositorio Git completo
   - Código documentado y limpio
   - Tests unitarios y de integración

2. **Documentación:**
   - README.md con guía de instalación y uso
   - Documentación técnica de arquitectura
   - Documentación de API interna
   - Guía de evaluación

3. **Resultados de Evaluación:**
   - Reporte de métricas en JSON
   - Gráficos de performance
   - Análisis de limitaciones

4. **Datos de Prueba:**
   - Dataset de 50 documentos de prueba
   - Ground truth anotado
   - Ejemplos de salida

5. **Configuración:**
   - Archivos de configuración
   - Templates de documentos
   - Scripts de setup

---

## 4. CONCLUSIONES

Este documento PRD+SRS define una arquitectura completa y detallada para un MVP funcional de un agente de clasificación y validación de documentos logísticos. El sistema propuesto:

✅ **Cumple los objetivos del proyecto:**
- Automatiza lectura, clasificación y validación
- Utiliza OCR y LLM locales
- Reduce errores manuales
- Mejora trazabilidad operativa

✅ **Es realizable como MVP:**
- Stack tecnológico probado y open source
- Alcance bien definido y acotado
- Métricas de éxito cuantificables
- Cronograma realista (6 semanas)

✅ **Es extensible:**
- Arquitectura modular
- Diseño preparado para integración futura
- Documentación de trabajo futuro clara

✅ **Ejecutable en VS Code con Claude Code:**
- CLI bien definida
- Configuración local
- Sin dependencias cloud obligatorias

---

## 5. REFERENCIAS

### 5.1 Tecnologías

- **PaddleOCR:** https://github.com/PaddlePaddle/PaddleOCR
- **Tesseract:** https://github.com/tesseract-ocr/tesseract
- **Ollama:** https://ollama.ai
- **Llama 3:** https://ai.meta.com/blog/meta-llama-3/
- **Pydantic:** https://docs.pydantic.dev
- **Typer:** https://typer.tiangolo.com

### 5.2 Papers y Recursos

- OCR para documentos: "Towards End-to-End Text Spotting in Natural Scenes" (PaddleOCR)
- LLM para extracción: "Large Language Models for Information Extraction"
- Validación de documentos: "Document Understanding with Vision and Language"

---

**Documento generado:** 2025-12-17  
**Versión:** 1.0  
**Autor:** Arquitectura diseñada por Claude (Anthropic)  
**Para:** MVP Agente de Clasificación de Documentos Logísticos

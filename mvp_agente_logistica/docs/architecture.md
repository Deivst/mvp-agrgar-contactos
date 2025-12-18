# Arquitectura del Sistema

## Vista General

El Agente de Clasificacion y Validacion de Documentos Logisticos sigue una arquitectura modular basada en pipelines, donde cada componente tiene responsabilidades bien definidas.

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
```

## Componentes Principales

### 1. Input Handler (`src/input/`)

Responsable de cargar y preparar documentos para procesamiento.

**Clases:**
- `DocumentLoader`: Carga imagenes y PDFs
- `ImagePreprocessor`: Preprocesa imagenes (denoise, deskew, enhance contrast)
- `InputValidator`: Valida formato, tamano y calidad

**Flujo:**
1. Validar archivo (formato, tamano, permisos)
2. Cargar documento (imagen o PDF)
3. Convertir PDF a imagenes si es necesario
4. Preprocesar imagen (pipeline configurable)

### 2. OCR Engine (`src/ocr/`)

Extrae texto de imagenes usando PaddleOCR con fallback a Tesseract.

**Clases:**
- `PaddleOCREngine`: Motor principal OCR
- `TesseractEngine`: Motor fallback
- Detectores adicionales (tablas, regiones) - TODO

**Caracteristicas:**
- Extraccion con coordenadas (bounding boxes)
- Niveles de confianza por bloque de texto
- Deteccion automatica de idioma
- Fallback automatico si el motor principal falla

### 3. LLM Engine (`src/llm/`)

Usa LLM local (Ollama) para clasificacion y extraccion estructurada.

**Clases:**
- `OllamaClient`: Cliente para comunicacion con Ollama
- `DocumentClassifier`: Clasifica tipo de documento
- `FieldExtractor`: Extrae campos estructurados

**Prompts:**
- Template de clasificacion
- Templates de extraccion por tipo de documento
- Sistema de reintentos con feedback de errores

### 4. Validator Engine (`src/validator/`) - TODO

Valida datos extraidos individual y cruzadamente.

**Componentes Planeados:**
- `CrossValidator`: Validacion cruzada entre documentos
- `RulesEngine`: Motor de reglas de negocio
- `DiscrepancyDetector`: Detector de discrepancias

### 5. Models (`src/models/`)

Schemas Pydantic para validacion de datos.

**Archivos:**
- `document.py`: Modelos geometricos (BBox, OCRResult)
- `fields.py`: Modelos de campos (Producto, Proveedor, Cliente)
- `schemas.py`: Schemas completos por tipo de documento

### 6. Core (`src/core/`)

Componentes centrales del sistema.

**Archivos:**
- `pipeline.py`: Orquestador principal
- `config.py`: Sistema de configuracion
- `logger.py`: Sistema de logging

### 7. CLI (`src/main.py`)

Interfaz de linea de comandos con Typer.

**Comandos:**
- `process`: Procesar documento individual
- `batch`: Procesar lote de documentos
- `config`: Gestionar configuracion
- `version`: Mostrar version

## Flujo de Datos

### Procesamiento de un Documento

```
1. [CLI] Usuario ejecuta comando
        ↓
2. [Config] Carga configuracion
        ↓
3. [Pipeline] Inicializa componentes
        ↓
4. [InputValidator] Valida archivo
        ↓
5. [DocumentLoader] Carga imagen/PDF
        ↓
6. [ImagePreprocessor] Preprocesa imagen
        ↓
7. [OCREngine] Extrae texto + coordenadas
        ↓
8. [DocumentClassifier] Clasifica tipo
        ↓
9. [FieldExtractor] Extrae campos estructurados
        ↓
10. [Pydantic] Valida datos con schema
        ↓
11. [ProcessedDocument] Crea objeto resultado
        ↓
12. [OutputHandler] Guarda JSON
        ↓
13. [CLI] Muestra resumen
```

## Patrones de Diseno

### 1. Strategy Pattern
- Motor OCR intercambiable (PaddleOCR vs Tesseract)
- Metodos de preprocesamiento configurables

### 2. Template Method
- Pipeline de procesamiento estandar
- Templates de prompts por tipo de documento

### 3. Singleton (Implicito)
- Cliente Ollama compartido
- Logger compartido

### 4. Factory (Implicito)
- Creacion de schemas segun tipo de documento
- Seleccion de prompts segun tipo

## Configuracion

El sistema usa un modelo jerarquico de configuracion:

1. **Archivo YAML** (`config.yaml`): Configuracion principal
2. **Variables de Entorno** (`.env`): Override de configuracion
3. **Argumentos CLI**: Override de runtime

Prioridad: CLI > .env > config.yaml > defaults

## Manejo de Errores

### Estrategia de Fallback

```
OCR:
  PaddleOCR (principal)
      ↓ (si falla)
  Tesseract (fallback)
      ↓ (si falla)
  RuntimeError

LLM:
  Intento 1
      ↓ (si falla validacion)
  Intento 2 (con feedback)
      ↓ (si falla validacion)
  Intento 3 (con feedback)
      ↓ (si falla)
  ValidationError
```

### Logging

- **DEBUG**: Detalles de procesamiento interno
- **INFO**: Progreso de operaciones principales
- **WARNING**: Situaciones recuperables (fallbacks, baja confianza)
- **ERROR**: Errores que impiden procesamiento

## Extensibilidad

### Agregar Nuevo Tipo de Documento

1. Crear template YAML en `templates/`
2. Crear schema Pydantic en `src/models/schemas.py`
3. Agregar enum en `DocumentType`
4. Crear prompt de extraccion en `src/llm/prompts.py`
5. Mapear en `FieldExtractor.schema_map`

### Agregar Nuevo Motor OCR

1. Crear clase en `src/ocr/nuevo_engine.py`
2. Implementar interfaz (metodo `extract_text`)
3. Configurar en `config.yaml`
4. Actualizar `Pipeline._execute_ocr()`

### Agregar Nueva Validacion

1. Crear regla en `src/validator/rules_engine.py`
2. Actualizar schema Pydantic con validator
3. Configurar severidad y accion sugerida

## Performance

### Cuellos de Botella

1. **OCR**: 5-15 segundos/documento
2. **LLM**: 3-10 segundos/documento (depende del modelo)
3. **Preprocesamiento**: <1 segundo/documento

### Optimizaciones Planeadas

- Cache de resultados OCR
- Procesamiento paralelo de lotes
- Uso de GPU para OCR y LLM
- Modelos LLM cuantizados mas rapidos

## Seguridad

- Procesamiento 100% local (sin envio de datos externos)
- Validacion de tamano de archivos
- Sanitizacion de rutas de archivo
- Validacion estricta con Pydantic

## Testing

### Estrategia de Testing

- **Unit Tests**: Cada componente individual
- **Integration Tests**: Pipeline completo
- **Fixtures**: Datos de prueba reutilizables

### Cobertura Objetivo

- Modelos Pydantic: >95%
- Core logic: >80%
- CLI: >70%

## Deployment

### Requisitos de Produccion

1. Servidor con Python 3.10+
2. Tesseract instalado
3. Ollama ejecutandose
4. Modelo LLM descargado
5. Configuracion ajustada

### Monitoreo Recomendado

- Tiempo de procesamiento por documento
- Tasa de exito/fallo
- Confianza promedio OCR
- Confianza promedio clasificacion
- Uso de recursos (CPU, RAM)

---

**Version:** 1.0.0
**Ultima actualizacion:** Diciembre 2025

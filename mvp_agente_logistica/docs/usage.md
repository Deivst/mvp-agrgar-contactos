# Guia de Uso del Agente Logistica MVP

## Inicio Rapido

### 1. Asegurate de que Ollama este ejecutandose

```bash
# Terminal 1: Iniciar Ollama
ollama serve
```

### 2. Activar entorno virtual

```bash
# Terminal 2: Activar venv
source venv/bin/activate  # macOS/Linux
# o
venv\Scripts\activate     # Windows
```

### 3. Procesar tu primer documento

```bash
python src/main.py process \
  --file ruta/al/documento.pdf \
  --output resultado.json \
  --verbose
```

## Comandos Disponibles

### `process` - Procesar Documento Individual

Procesa un solo documento y extrae sus campos.

**Sintaxis:**
```bash
python src/main.py process [OPCIONES]
```

**Opciones:**

| Opcion | Descripcion | Requerido |
|--------|-------------|-----------|
| `--file`, `-f` | Ruta al documento | Si |
| `--output`, `-o` | Ruta del archivo JSON de salida | No |
| `--config`, `-c` | Archivo de configuracion custom | No |
| `--verbose`, `-v` | Modo verbose (mas logs) | No |
| `--quiet`, `-q` | Modo silencioso (solo errores) | No |

**Ejemplos:**

```bash
# Basico
python src/main.py process --file albaran.pdf

# Con archivo de salida
python src/main.py process --file albaran.pdf --output result.json

# Modo verbose
python src/main.py process --file albaran.pdf --verbose

# Con configuracion custom
python src/main.py process --file albaran.pdf --config custom_config.yaml
```

**Salida:**

```
Procesando documento: albaran.pdf

[1/7] Validando documento...
[2/7] Cargando documento...
[3/7] Preprocesando imagen...
[4/7] Ejecutando OCR...
[5/7] Clasificando documento...
[6/7] Extrayendo campos estructurados...
[7/7] Generando resultado...

Documento procesado exitosamente!

┌─────────────────────────┬───────────────────┐
│ Campo                   │ Valor             │
├─────────────────────────┼───────────────────┤
│ Tipo de Documento       │ ALBARAN           │
│ Confianza Clasificacion │ 95.00%            │
│ Confianza OCR           │ 92.50%            │
│ Motor OCR               │ PaddleOCR         │
│ Bloques de Texto        │ 47                │
│ Tiempo de Procesamiento │ 26.30s            │
│ Archivo de Salida       │ result.json       │
└─────────────────────────┴───────────────────┘
```

### `batch` - Procesar Lote de Documentos

Procesa multiples documentos de un directorio.

**Sintaxis:**
```bash
python src/main.py batch [OPCIONES]
```

**Opciones:**

| Opcion | Descripcion | Requerido |
|--------|-------------|-----------|
| `--input-dir`, `-i` | Directorio con documentos | Si |
| `--output-dir`, `-o` | Directorio de salida | Si |
| `--pattern`, `-p` | Patron de archivos (default: `*.*`) | No |
| `--config`, `-c` | Archivo de configuracion custom | No |
| `--verbose`, `-v` | Modo verbose | No |

**Ejemplos:**

```bash
# Procesar todos los archivos
python src/main.py batch \
  --input-dir data/raw/ \
  --output-dir data/processed/

# Solo PDFs
python src/main.py batch \
  --input-dir data/raw/ \
  --output-dir data/processed/ \
  --pattern "*.pdf"

# Solo imagenes
python src/main.py batch \
  --input-dir data/raw/ \
  --output-dir data/processed/ \
  --pattern "*.{jpg,png}"
```

**Salida:**

```
Procesando 15 documentos...

--- Procesando documento 1/15 ---
Documento procesado exitosamente!

--- Procesando documento 2/15 ---
Documento procesado exitosamente!

...

Lote completado: 14/15 documentos procesados
```

### `config` - Gestionar Configuracion

Muestra o edita la configuracion del sistema.

**Sintaxis:**
```bash
python src/main.py config [OPCIONES]
```

**Opciones:**

| Opcion | Descripcion |
|--------|-------------|
| `--show` | Muestra configuracion actual |
| `--config`, `-c` | Archivo de configuracion custom |

**Ejemplos:**

```bash
# Mostrar configuracion actual
python src/main.py config --show

# Mostrar configuracion custom
python src/main.py config --show --config custom_config.yaml
```

### `version` - Mostrar Version

Muestra la version del agente.

```bash
python src/main.py version

# Salida:
# Agente Logistica MVP v1.0.0
```

## Formato de Salida JSON

El sistema genera archivos JSON con la siguiente estructura:

```json
{
  "file_path": "data/raw/albaran_001.pdf",
  "file_name": "albaran_001.pdf",
  "file_size_kb": 245.0,
  "processing_timestamp": "2025-12-17T14:30:26",
  "processing_time_seconds": 26.3,
  "agent_version": "1.0.0",
  "document_type": "ALBARAN",
  "classification_confidence": 0.95,
  "ocr_engine_used": "PaddleOCR",
  "ocr_average_confidence": 0.925,
  "total_text_blocks": 47,
  "tables_detected": 1,
  "signatures_detected": true,
  "stamps_detected": true,
  "extracted_fields": {
    "numero_albaran": "ALB-20250115",
    "fecha_emision": "2025-01-15",
    "proveedor": {
      "razon_social": "Distribuciones Lopez S.L.",
      "cif": "B12345678",
      "direccion": "Calle Mayor 123, Madrid"
    },
    "cliente": {
      "razon_social": "Farmacia Garcia",
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
      }
    ],
    "total": 429.00,
    "firma_transportista": true,
    "sello_empresa": true,
    "observaciones": null
  },
  "validation_status": "valid",
  "validation_errors": [],
  "validation_warnings": [],
  "raw_ocr_text": "ALBARAN DE ENTREGA..."
}
```

## Personalizacion de Configuracion

### Modificar `config.yaml`

Puedes ajustar el comportamiento del sistema editando `config.yaml`:

```yaml
# Ejemplo: Cambiar modelo LLM
llm:
  model: "mistral:7b"  # Cambia de llama3:8b a mistral:7b

# Ejemplo: Desactivar preprocesamiento
preprocessing:
  denoise: false
  deskew: false

# Ejemplo: Cambiar umbral de confianza OCR
ocr:
  confidence_threshold: 0.8  # Aumenta de 0.7 a 0.8
```

### Usar Configuracion Custom

```bash
# Crear config custom
cp config.yaml mi_config.yaml

# Editar mi_config.yaml con tus cambios

# Usar config custom
python src/main.py process \
  --file documento.pdf \
  --config mi_config.yaml
```

## Tips y Mejores Practicas

### 1. Optimizar Calidad de Imagenes

**Problema**: OCR con baja confianza

**Soluciones**:
- Asegurar resolucion minima de 150 DPI
- Usar imagenes con buen contraste
- Evitar imagenes borrosas o muy comprimidas

### 2. Acelerar Procesamiento

**Opciones**:
- Habilitar GPU en `config.yaml` (si tienes GPU)
- Usar modelo LLM mas pequeno (llama3:1b en lugar de llama3:8b)
- Desactivar `include_raw_ocr` en configuracion

```yaml
# config.yaml
ocr:
  use_gpu: true

llm:
  model: "llama3:1b"  # Mas rapido pero menos preciso

output:
  include_raw_ocr: false  # Reduce tamano de JSON
```

### 3. Mejorar Precision de Extraccion

**Opciones**:
- Usar modelo LLM mas grande (llama3:13b)
- Reducir temperature para respuestas mas deterministas
- Aumentar max_retries para extraccion

```yaml
# config.yaml
llm:
  model: "llama3:13b"
  temperature: 0.05  # Mas deterministico

  extraction:
    max_retries: 3  # Mas reintentos
```

### 4. Procesar Documentos en Paralelo (Futuro)

Actualmente el MVP procesa documentos secuencialmente. Para procesamiento paralelo:

```python
# Ejemplo de implementacion futura
from multiprocessing import Pool

def process_file(file_path):
    return pipeline.process_document(file_path)

with Pool(processes=4) as pool:
    results = pool.map(process_file, file_paths)
```

### 5. Debugging

**Modo verbose:**
```bash
python src/main.py process --file documento.pdf --verbose
```

**Ver logs:**
```bash
tail -f logs/agente.log
```

**Guardar logs en archivo especifico:**
```bash
python src/main.py process --file documento.pdf --verbose 2>&1 | tee mi_log.txt
```

## Casos de Uso Comunes

### Caso 1: Digitalizar Albaranes de Entrega

```bash
# Procesar todos los albaranes del mes
python src/main.py batch \
  --input-dir escaneos/enero_2025/ \
  --output-dir procesados/enero_2025/ \
  --pattern "albaran_*.pdf" \
  --verbose
```

### Caso 2: Extraer Datos de Ordenes de Envio

```bash
# Procesar orden individual
python src/main.py process \
  --file ordenes/ORD-20250115.pdf \
  --output datos/orden_20250115.json
```

### Caso 3: Validar Notas de Recepcion

```bash
# Procesar notas de recepcion
python src/main.py batch \
  --input-dir recepciones/ \
  --output-dir resultados/recepciones/ \
  --pattern "REC-*.pdf"

# TODO: Validacion cruzada (no implementado en MVP)
# python src/main.py validate --group resultados/recepciones/*.json
```

## Solucion de Problemas

Ver seccion **Troubleshooting** en README.md

---

**Version:** 1.0.0
**Ultima actualizacion:** Diciembre 2025

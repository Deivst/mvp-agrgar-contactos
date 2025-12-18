# Agente de Clasificacion y Validacion de Documentos Logisticos - MVP

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

Sistema de IA local para automatizar la lectura, clasificacion, extraccion y validacion de campos clave en documentacion logistica mediante OCR (PaddleOCR/Tesseract) y modelos de lenguaje locales (Ollama + Llama 3).

## Caracteristicas Principales

- **Clasificacion Automatica**: Identifica 4 tipos de documentos (Albaran, Orden de Envio, Nota de Recepcion, Parte de Transporte)
- **OCR Robusto**: PaddleOCR como motor principal con fallback a Tesseract
- **Extraccion Estructurada**: Extrae 10+ campos clave por tipo de documento usando LLM local
- **Procesamiento Local**: Sin dependencias cloud, ejecucion 100% local
- **Validacion de Datos**: Validacion individual de campos con Pydantic
- **CLI Intuitiva**: Interfaz de linea de comandos con Typer

## Tipos de Documentos Soportados

1. **Albaran de Entrega**: Documento de entrega de mercancias
2. **Orden de Envio**: Instruccion de despacho o envio
3. **Nota de Recepcion**: Comprobante de recepcion de mercancias
4. **Parte de Transporte**: Documento de control de transporte

## Requisitos del Sistema

### Requisitos Minimos

- **OS**: Windows 10+, macOS 11+, Ubuntu 20.04+
- **Python**: 3.10 o superior
- **RAM**: 8GB (16GB recomendado)
- **Almacenamiento**: 5GB libres
- **CPU**: 4 cores (8 recomendado)
- **GPU**: Opcional (acelera OCR y LLM)

### Software Requerido

- Python 3.10+
- Tesseract OCR 5.3+
- Ollama (para LLM local)
- Git

## Instalacion

### 1. Clonar el Repositorio

```bash
git clone <repository-url>
cd mvp_agente_logistica
```

### 2. Crear Entorno Virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Instalar Dependencias Python

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Instalar Tesseract OCR

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-spa
```

**macOS:**
```bash
brew install tesseract tesseract-lang
```

**Windows:**
1. Descargar instalador desde: https://github.com/UB-Mannheim/tesseract/wiki
2. Instalar y agregar al PATH

### 5. Instalar Ollama y Descargar Modelo

**Instalar Ollama:**
```bash
# macOS/Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows: Descargar desde https://ollama.ai
```

**Descargar modelo LLM:**
```bash
ollama pull llama3:8b
```

### 6. Configurar Variables de Entorno

```bash
cp .env.example .env
# Editar .env con tus rutas si es necesario
```

### 7. Verificar Instalacion

Verifica que Ollama este ejecutandose:
```bash
ollama serve
```

En otra terminal, prueba el sistema:
```bash
python src/main.py version
```

## Uso

### Procesar un Documento Individual

```bash
python src/main.py process \
  --file data/raw/albaran_001.pdf \
  --output data/processed/albaran_001.json \
  --verbose
```

### Procesar un Lote de Documentos

```bash
python src/main.py batch \
  --input-dir data/raw/ \
  --output-dir data/processed/ \
  --pattern "*.pdf" \
  --verbose
```

### Ver Configuracion Actual

```bash
python src/main.py config --show
```

### Opciones Disponibles

```
--file, -f PATH         Ruta al documento a procesar
--output, -o PATH       Ruta del archivo de salida JSON
--config, -c PATH       Archivo de configuracion custom
--verbose, -v           Modo verbose (logs detallados)
--quiet, -q            Modo silencioso (solo errores)
--help                 Muestra ayuda
```

## Estructura del Proyecto

```
mvp_agente_logistica/
├── src/
│   ├── core/              # Pipeline, config, logger
│   ├── input/             # Carga y preprocesamiento
│   ├── ocr/               # Motores OCR
│   ├── llm/               # Cliente LLM, clasificacion, extraccion
│   ├── validator/         # Validacion (TODO)
│   ├── output/            # Exportacion (TODO)
│   ├── models/            # Schemas Pydantic
│   └── main.py            # CLI principal
├── templates/             # Templates YAML por tipo documento
├── data/
│   ├── raw/              # Documentos sin procesar
│   ├── processed/        # Documentos procesados (JSON)
│   ├── test/             # Dataset de prueba
│   └── results/          # Reportes y metricas
├── tests/                # Tests automatizados
├── docs/                 # Documentacion
├── config.yaml           # Configuracion principal
├── requirements.txt      # Dependencias Python
└── README.md            # Este archivo
```

## Formato de Salida JSON

Ejemplo de documento procesado:

```json
{
  "file_path": "data/raw/albaran_001.pdf",
  "file_name": "albaran_001.pdf",
  "processing_timestamp": "2025-12-17T14:30:26Z",
  "document_type": "ALBARAN",
  "classification_confidence": 0.95,
  "ocr_average_confidence": 0.925,
  "extracted_fields": {
    "numero_albaran": "ALB-20250115",
    "fecha_emision": "2025-01-15",
    "proveedor": {
      "razon_social": "Distribuciones Lopez S.L.",
      "cif": "B12345678"
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
    "total": 225.00
  }
}
```

## Configuracion

El sistema se configura mediante `config.yaml`. Principales opciones:

```yaml
# OCR
ocr:
  primary_engine: "paddleocr"
  fallback_engine: "tesseract"
  confidence_threshold: 0.7

# LLM
llm:
  model: "llama3:8b"
  base_url: "http://localhost:11434"
  temperature: 0.1

# Preprocesamiento
preprocessing:
  denoise: true
  deskew: true
  enhance_contrast: true
```

## Metricas de Exito (Objetivos MVP)

| Metrica | Objetivo | Status |
|---------|----------|--------|
| Precision OCR | >85% | ⏳ En evaluacion |
| F1-Score Extraccion | >80% | ⏳ En evaluacion |
| Clasificacion Correcta | >90% | ⏳ En evaluacion |
| Tiempo de Procesamiento | <30s/doc | ⏳ En evaluacion |

## Limitaciones del MVP

- Solo texto impreso (no manuscrito)
- Idioma: Español unicamente
- Sin validacion cruzada entre documentos (TODO)
- Sin API REST (solo CLI)
- Procesamiento secuencial (sin paralelizacion)

## Trabajo Futuro

- [ ] Validacion cruzada entre documentos relacionados
- [ ] Soporte para escritura manual
- [ ] Multi-idioma (ingles, portugues)
- [ ] API REST para integracion
- [ ] Dashboard web para supervision
- [ ] Mejora de deteccion de tablas
- [ ] Sistema de aprendizaje continuo

## Troubleshooting

### Error: "No se pudo conectar con Ollama"

**Solucion**: Asegurate de que Ollama este ejecutandose:
```bash
ollama serve
```

### Error: "PaddleOCR failed"

**Solucion**: El sistema usara Tesseract automaticamente como fallback. Verifica que Tesseract este instalado:
```bash
tesseract --version
```

### Error: "Modelo llama3:8b no encontrado"

**Solucion**: Descarga el modelo:
```bash
ollama pull llama3:8b
```

### Rendimiento Lento

**Soluciones**:
1. Reduce el tamano de las imagenes antes de procesarlas
2. Habilita GPU en config.yaml si tienes GPU disponible
3. Usa un modelo LLM mas pequeno (ej: llama3:1b)

## Contribuciones

Este es un proyecto MVP. Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## Licencia

MIT License - Ver archivo LICENSE para detalles

## Autor

Desarrollado para automatizacion de procesos logisticos

---

**Documentacion Adicional:**
- [Guia de Instalacion Detallada](docs/setup.md)
- [Guia de Uso](docs/usage.md)
- [Arquitectura del Sistema](docs/architecture.md)

**Version:** 1.0.0
**Fecha:** Diciembre 2025

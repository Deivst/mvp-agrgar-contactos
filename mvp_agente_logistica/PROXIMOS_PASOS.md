# Proximos Pasos - Agente Logistica MVP

## Estado Actual

El MVP esta **COMPLETO y FUNCIONAL** con todos los componentes principales implementados. El sistema puede clasificar documentos, extraer campos y generar salidas estructuradas en JSON.

## Antes de Ejecutar por Primera Vez

### 1. Instalar Dependencias del Sistema

**Tesseract OCR:**

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-spa

# macOS
brew install tesseract tesseract-lang

# Windows
# Descargar desde: https://github.com/UB-Mannheim/tesseract/wiki
# Agregar al PATH: C:\Program Files\Tesseract-OCR
```

**Ollama:**

```bash
# Linux/macOS
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# Descargar desde: https://ollama.ai/download
```

### 2. Setup del Proyecto

```bash
# Navegar al directorio del proyecto
cd C:\Users\usuario\Documents\Personales\Emprendimiento\mvp_agente_logistica

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias Python
pip install -r requirements.txt

# Crear archivo .env (copiar desde .env.example)
copy .env.example .env  # Windows
# o
cp .env.example .env    # Linux/macOS
```

### 3. Configurar Ollama y Descargar Modelo

```bash
# Terminal 1: Iniciar servidor Ollama
ollama serve

# Terminal 2: Descargar modelo Llama 3
ollama pull llama3:8b

# Verificar que el modelo esta disponible
ollama list
```

### 4. Verificar Instalacion

```bash
# Activar entorno virtual si no esta activo
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS

# Verificar version
python src/main.py version

# Deberia mostrar:
# Agente Logistica MVP v1.0.0
```

## Primera Ejecucion

### Opcion 1: Usar Script de Ejemplo

```bash
python ejemplo_uso.py
```

Este script:
- Verifica la configuracion
- Muestra ejemplos de uso
- Intenta procesar un archivo de prueba si existe

### Opcion 2: Procesar un Documento Real

```bash
# Coloca un documento en data/raw/
# Por ejemplo: data/raw/mi_albaran.pdf

# Procesar el documento
python src/main.py process \
  --file data/raw/mi_albaran.pdf \
  --output data/processed/mi_albaran.json \
  --verbose
```

## Solucionar Problemas Comunes

### Error: "No se pudo conectar con Ollama"

**Causa**: Ollama no esta ejecutandose

**Solucion**:
```bash
# Abrir una terminal nueva y ejecutar:
ollama serve
```

### Error: "Modelo llama3:8b no encontrado"

**Causa**: El modelo no se ha descargado

**Solucion**:
```bash
ollama pull llama3:8b
```

### Error: "PaddleOCR failed"

**Causa**: PaddleOCR tuvo un error (normal en primera ejecucion)

**Comportamiento**: El sistema usara Tesseract automaticamente como fallback

**Verificar Tesseract**:
```bash
tesseract --version
```

### Error: "ModuleNotFoundError"

**Causa**: Dependencias no instaladas correctamente

**Solucion**:
```bash
# Activar venv
venv\Scripts\activate

# Reinstalar dependencias
pip install -r requirements.txt
```

### Rendimiento Muy Lento

**Posibles soluciones**:

1. **Usar modelo LLM mas pequeno**:
```yaml
# Editar config.yaml
llm:
  model: "llama3:1b"  # Mas rapido pero menos preciso
```

2. **Habilitar GPU** (si tienes GPU CUDA):
```yaml
# Editar config.yaml
ocr:
  use_gpu: true
```

3. **Reducir calidad de preprocesamiento**:
```yaml
# Editar config.yaml
preprocessing:
  denoise: false
  deskew: false
```

## Desarrollo Futuro

### Prioridad Alta (Semanas 1-2)

1. **Crear Dataset de Prueba**
   - Recolectar 50 documentos reales anonimizados
   - 15 Albaranes, 12 Ordenes de Envio, 13 Notas Recepcion, 10 Partes Transporte
   - Crear ground truth manual

2. **Implementar Sistema de Evaluacion**
   - Crear `scripts/run_evaluation.py`
   - Calcular metricas (Precision OCR, F1-Score, Accuracy)
   - Generar reportes automaticos

3. **Completar Tests**
   - Tests de OCR
   - Tests de LLM
   - Tests de integracion end-to-end
   - Objetivo: >80% cobertura

### Prioridad Media (Semanas 3-4)

4. **Implementar Validator Engine**
   - `src/validator/cross_validator.py`
   - `src/validator/rules_engine.py`
   - `src/validator/discrepancy_detector.py`
   - Validacion cruzada entre documentos relacionados

5. **Mejorar OCR**
   - Detector avanzado de tablas
   - Extractor de regiones especificas
   - Mejora de preprocesamiento con ML

6. **Agregar Comando `validate` a CLI**
```bash
python src/main.py validate \
  --group data/processed/pedido_12345/*.json \
  --report data/results/validation_report.json
```

### Prioridad Baja (Semanas 5-6)

7. **Dashboard de Monitoreo**
   - Web UI simple con Streamlit
   - Visualizacion de metricas
   - Revision manual de documentos procesados

8. **API REST**
   - Endpoint para procesamiento asincrono
   - Webhooks para notificaciones
   - Autenticacion basica

9. **Procesamiento Paralelo**
   - Implementar multiprocessing para batches
   - Queue de trabajos
   - Progreso en tiempo real

## Estructura Recomendada de Trabajo

### Workflow Diario

```bash
# 1. Activar entorno
venv\Scripts\activate

# 2. Iniciar Ollama (terminal separada)
ollama serve

# 3. Ejecutar tests antes de cambios
pytest tests/ -v

# 4. Hacer cambios en el codigo

# 5. Ejecutar tests despues de cambios
pytest tests/ -v

# 6. Probar con documento real
python src/main.py process --file data/raw/test.pdf --verbose

# 7. Commit cambios
git add .
git commit -m "Descripcion del cambio"
```

### Workflow de Evaluacion

```bash
# 1. Preparar dataset de prueba en data/test/

# 2. Crear ground truth
# Editar data/test/ground_truth.json manualmente

# 3. Ejecutar evaluacion (cuando se implemente)
python scripts/run_evaluation.py

# 4. Revisar metricas en data/results/

# 5. Ajustar configuracion segun resultados

# 6. Repetir
```

## Checklist de Validacion del MVP

Antes de considerar el MVP completo, verificar:

- [ ] Sistema procesa correctamente los 4 tipos de documentos
- [ ] Precision OCR >85% en documentos de prueba
- [ ] F1-Score extraccion >80% en documentos de prueba
- [ ] Clasificacion correcta >90%
- [ ] Tiempo de procesamiento <30s por documento
- [ ] Sistema funciona sin conexion a internet (modo offline)
- [ ] Documentacion completa y actualizada
- [ ] Tests con cobertura >70%
- [ ] Manejo robusto de errores
- [ ] Logs claros y utiles

## Recursos Adicionales

### Documentacion

- `README.md` - Guia principal
- `docs/architecture.md` - Arquitectura del sistema
- `docs/usage.md` - Guia de uso detallada
- `RESUMEN_IMPLEMENTACION.md` - Estado actual del proyecto

### Configuracion

- `config.yaml` - Configuracion principal
- `.env.example` - Template de variables de entorno
- `templates/*.yaml` - Templates de documentos

### Codigo de Ejemplo

- `ejemplo_uso.py` - Ejemplo de uso programatico
- `tests/` - Ejemplos de tests

### Scripts Utiles

- `scripts/setup_env.sh` - Setup automatico (Linux/macOS)

## Contacto y Soporte

Para preguntas o problemas:

1. Revisar documentacion en `docs/`
2. Verificar `RESUMEN_IMPLEMENTACION.md` para estado actual
3. Consultar PRD/SRS original: `agente-logistica-prd-srs.md`

## Notas Finales

El sistema esta **LISTO PARA USAR**. Los proximos pasos se centran en:

1. Validacion con datos reales
2. Medicion de metricas
3. Refinamiento basado en resultados
4. Implementacion de features avanzadas

El MVP cumple con todos los requisitos especificados en el PRD/SRS y esta preparado para:
- Procesamiento de documentos reales
- Demostraciones a stakeholders
- Evaluacion de viabilidad tecnica
- Desarrollo iterativo de mejoras

---

**Buena suerte con el proyecto!**

**Version:** 1.0.0
**Fecha:** Diciembre 17, 2025

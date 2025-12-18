#!/bin/bash

# Script de setup del entorno para el Agente Logistica MVP

echo "================================================"
echo "Setup del Agente de Documentos Logisticos - MVP"
echo "================================================"

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar Python
echo -e "\n${YELLOW}[1/6]${NC} Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} Python encontrado: $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python 3 no encontrado. Instala Python 3.10 o superior"
    exit 1
fi

# Crear entorno virtual
echo -e "\n${YELLOW}[2/6]${NC} Creando entorno virtual..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Entorno virtual creado"
else
    echo -e "${GREEN}✓${NC} Entorno virtual ya existe"
fi

# Activar entorno virtual
echo -e "\n${YELLOW}[3/6]${NC} Activando entorno virtual..."
source venv/bin/activate
echo -e "${GREEN}✓${NC} Entorno virtual activado"

# Instalar dependencias
echo -e "\n${YELLOW}[4/6]${NC} Instalando dependencias Python..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo -e "${GREEN}✓${NC} Dependencias instaladas"

# Verificar Tesseract
echo -e "\n${YELLOW}[5/6]${NC} Verificando Tesseract OCR..."
if command -v tesseract &> /dev/null; then
    TESSERACT_VERSION=$(tesseract --version 2>&1 | head -n 1)
    echo -e "${GREEN}✓${NC} Tesseract encontrado: $TESSERACT_VERSION"
else
    echo -e "${YELLOW}⚠${NC} Tesseract no encontrado"
    echo "  Instala Tesseract:"
    echo "  - Ubuntu/Debian: sudo apt-get install tesseract-ocr tesseract-ocr-spa"
    echo "  - macOS: brew install tesseract tesseract-lang"
fi

# Verificar Ollama
echo -e "\n${YELLOW}[6/6]${NC} Verificando Ollama..."
if command -v ollama &> /dev/null; then
    echo -e "${GREEN}✓${NC} Ollama encontrado"

    # Verificar que Ollama este ejecutandose
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC} Ollama esta ejecutandose"

        # Verificar modelo llama3
        if ollama list | grep -q "llama3"; then
            echo -e "${GREEN}✓${NC} Modelo llama3 instalado"
        else
            echo -e "${YELLOW}⚠${NC} Modelo llama3 no encontrado"
            echo "  Descarga el modelo con: ollama pull llama3:8b"
        fi
    else
        echo -e "${YELLOW}⚠${NC} Ollama no esta ejecutandose"
        echo "  Inicia Ollama con: ollama serve"
    fi
else
    echo -e "${YELLOW}⚠${NC} Ollama no encontrado"
    echo "  Instala Ollama desde: https://ollama.ai"
fi

# Crear directorios
echo -e "\n${YELLOW}Creando directorios necesarios...${NC}"
mkdir -p data/raw data/processed data/test data/results logs cache
echo -e "${GREEN}✓${NC} Directorios creados"

# Copiar .env.example a .env si no existe
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "${GREEN}✓${NC} Archivo .env creado"
fi

echo -e "\n${GREEN}================================================${NC}"
echo -e "${GREEN}Setup completado exitosamente!${NC}"
echo -e "${GREEN}================================================${NC}"

echo -e "\nPara activar el entorno virtual en el futuro:"
echo -e "  ${YELLOW}source venv/bin/activate${NC}"

echo -e "\nPara probar el sistema:"
echo -e "  ${YELLOW}python src/main.py version${NC}"

echo -e "\nPara procesar un documento:"
echo -e "  ${YELLOW}python src/main.py process --file ruta/al/documento.pdf --output resultado.json${NC}"

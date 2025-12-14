#!/bin/bash

# ================================================
# Quick Start Script
# Sistema Multi-Agente de Gestión de Contactos
# ================================================

set -e

echo "================================================"
echo "Sistema Multi-Agente de Gestión de Contactos"
echo "Iniciando configuración..."
echo "================================================"
echo ""

# Verificar que existe .env
if [ ! -f .env ]; then
    echo "⚠️  No se encontró archivo .env"
    echo "📝 Copiando .env.example a .env..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANTE: Edita el archivo .env con tus credenciales:"
    echo "   - TELEGRAM_BOT_TOKEN"
    echo "   - TELEGRAM_ALLOWED_USERS"
    echo "   - GEMINI_API_KEY"
    echo ""
    echo "Después ejecuta este script nuevamente."
    exit 1
fi

# Verificar que las variables críticas estén configuradas
source .env

if [ "$TELEGRAM_BOT_TOKEN" = "your_telegram_bot_token_here" ] || \
   [ "$GEMINI_API_KEY" = "your_gemini_api_key_here" ]; then
    echo "❌ Error: Debes configurar las credenciales en .env"
    echo ""
    echo "Edita .env y configura:"
    echo "  - TELEGRAM_BOT_TOKEN (obtenido de @BotFather)"
    echo "  - GEMINI_API_KEY (de https://ai.google.dev/)"
    echo "  - TELEGRAM_ALLOWED_USERS (tu user ID de Telegram)"
    echo ""
    exit 1
fi

echo "✅ Archivo .env configurado correctamente"
echo ""

# Preguntar método de instalación
echo "¿Cómo deseas ejecutar el sistema?"
echo "1) Docker (recomendado)"
echo "2) Instalación local"
read -p "Selecciona una opción (1 o 2): " option
echo ""

if [ "$option" = "1" ]; then
    # Docker
    echo "🐳 Iniciando con Docker..."
    echo ""

    # Verificar Docker
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker no está instalado"
        echo "Instálalo desde: https://docs.docker.com/get-docker/"
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose no está instalado"
        echo "Instálalo desde: https://docs.docker.com/compose/install/"
        exit 1
    fi

    echo "🏗️  Construyendo imágenes..."
    docker-compose build

    echo ""
    echo "🚀 Iniciando servicios..."
    docker-compose up -d

    echo ""
    echo "⏳ Esperando que los servicios estén listos..."
    sleep 5

    echo ""
    echo "📊 Estado de los servicios:"
    docker-compose ps

    echo ""
    echo "✅ Sistema iniciado correctamente!"
    echo ""
    echo "📝 Comandos útiles:"
    echo "   Ver logs:        docker-compose logs -f bot"
    echo "   Detener:         docker-compose down"
    echo "   Reiniciar:       docker-compose restart bot"
    echo "   Ver BD:          http://localhost:5050 (pgAdmin)"
    echo ""

elif [ "$option" = "2" ]; then
    # Local
    echo "💻 Instalación local..."
    echo ""

    # Verificar Python
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python 3 no está instalado"
        exit 1
    fi

    python_version=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    echo "✅ Python $python_version detectado"

    # Crear entorno virtual si no existe
    if [ ! -d "venv" ]; then
        echo "📦 Creando entorno virtual..."
        python3 -m venv venv
    fi

    # Activar entorno virtual
    echo "🔌 Activando entorno virtual..."
    source venv/bin/activate

    # Instalar dependencias
    echo "📥 Instalando dependencias..."
    pip install -q --upgrade pip
    pip install -q -r requirements.txt

    # Verificar PostgreSQL
    echo ""
    echo "⚠️  IMPORTANTE: Asegúrate de que PostgreSQL esté corriendo"
    echo "   y que DATABASE_URL en .env esté configurado correctamente"
    echo ""
    read -p "¿PostgreSQL está corriendo? (s/n): " pg_running

    if [ "$pg_running" != "s" ]; then
        echo ""
        echo "Inicia PostgreSQL e intenta nuevamente."
        exit 1
    fi

    # Inicializar BD
    echo ""
    echo "🗄️  Inicializando base de datos..."
    python scripts/init_db.py

    # Iniciar bot
    echo ""
    echo "🚀 Iniciando bot..."
    echo ""
    echo "Presiona Ctrl+C para detener"
    echo ""
    python main.py

else
    echo "❌ Opción inválida"
    exit 1
fi

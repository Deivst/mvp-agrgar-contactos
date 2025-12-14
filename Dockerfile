# ================================================
# Dockerfile - Sistema Multi-Agente de Gestión de Contactos
# ================================================

FROM python:3.11-slim

# Metadata
LABEL maintainer="your-email@example.com"
LABEL description="Sistema Multi-Agente de Gestión de Contactos con Telegram y Google Gemini"

# Establecer directorio de trabajo
WORKDIR /app

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements.txt
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copiar código de la aplicación
COPY src/ ./src/
COPY config/ ./config/
COPY scripts/ ./scripts/
COPY main.py .

# Crear directorio de logs
RUN mkdir -p logs

# Crear usuario no-root para ejecutar la aplicación
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Cambiar a usuario no-root
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Comando de ejecución
CMD ["python", "main.py"]

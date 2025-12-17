# Script de Setup Completo - PostgreSQL + Bot
# Uso: .\run_setup.ps1

Write-Host "========================================" -ForegroundColor Green
Write-Host "Setup Completo - Sistema de Contactos" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Variables
$POSTGRES_PATH = "C:\Program Files\PostgreSQL\18\bin\psql.exe"
$POSTGRES_PASSWORD = "Moog22002"
$PROJECT_DIR = "c:\Users\usuario\Documents\Personales\Emprendimiento\mvp-agrgar-contactos"

# 1. Activar entorno virtual
Write-Host "[1/5] Activando entorno virtual..." -ForegroundColor Cyan
cd $PROJECT_DIR
.\venv\Scripts\Activate

# 2. Instalar psycopg2 si no está instalado
Write-Host "[2/5] Verificando psycopg2-binary..." -ForegroundColor Cyan
$env:PGPASSWORD = $POSTGRES_PASSWORD
.\venv\Scripts\pip install psycopg2-binary -q

# 3. Verificar conexión a PostgreSQL
Write-Host "[3/5] Verificando conexión a PostgreSQL..." -ForegroundColor Cyan
$env:PGPASSWORD = $POSTGRES_PASSWORD
& $POSTGRES_PATH -U postgres -h localhost -c "SELECT version();" | Out-Null
if ($LASTEXITCODE -eq 0) {
    Write-Host "    ✓ Conexión a PostgreSQL exitosa" -ForegroundColor Green
} else {
    Write-Host "    ✗ Error: No se pudo conectar a PostgreSQL" -ForegroundColor Red
    exit 1
}

# 4. Inicializar base de datos (crear tablas)
Write-Host "[4/5] Inicializando base de datos..." -ForegroundColor Cyan
.\venv\Scripts\python scripts/init_db.py
if ($LASTEXITCODE -ne 0) {
    Write-Host "    ✗ Error al inicializar la BD" -ForegroundColor Red
    exit 1
}

# 5. Ejecutar el bot
Write-Host "[5/5] Iniciando el bot..." -ForegroundColor Cyan
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✓ Setup completado exitosamente" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "El bot está iniciando..." -ForegroundColor Yellow
Write-Host "Envía mensajes a tu bot de Telegram para probar" -ForegroundColor Yellow
Write-Host ""
Write-Host "Presiona Ctrl+C para detener el bot" -ForegroundColor Yellow
Write-Host ""

.\venv\Scripts\python main.py

# Guía de Despliegue

## Pasos Rápidos para Empezar

### 1. Obtener Credenciales

#### Bot de Telegram

1. Abre Telegram y busca `@BotFather`
2. Envía el comando `/newbot`
3. Sigue las instrucciones para crear tu bot
4. Copia el **token** que te proporciona
5. Para obtener tu **user ID**, envía un mensaje a `@userinfobot`

#### Google Gemini API

1. Ve a https://ai.google.dev/
2. Crea una cuenta o inicia sesión
3. Ve a "Get API key"
4. Crea una nueva API key
5. Copia la key generada

### 2. Configuración

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar con tus credenciales
nano .env  # o vim .env, o code .env
```

Configurar en `.env`:

```env
# OBLIGATORIO - Token de @BotFather
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz

# OBLIGATORIO - Tu user ID (de @userinfobot)
TELEGRAM_ALLOWED_USERS=123456789

# OBLIGATORIO - API key de Gemini
GEMINI_API_KEY=AIzaSy...

# OBLIGATORIO - URL de PostgreSQL
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/contacts_db
```

### 3. Ejecutar con Docker (Recomendado)

```bash
# Iniciar servicios
docker-compose up -d

# Ver logs
docker-compose logs -f bot

# Verificar estado
docker-compose ps
```

### 4. Probar el Bot

1. Abre Telegram
2. Busca tu bot por el nombre que le diste
3. Envía `/start`
4. Prueba enviando un contacto:
   ```
   Juan Pérez 3001234567 recomendado por María
   ```

## Instalación Local (Sin Docker)

### Prerequisitos

- Python 3.10+
- PostgreSQL 12+

### Pasos

```bash
# 1. Crear entorno virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# o
.\venv\Scripts\activate  # Windows

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Crear base de datos
# Primero, crear la base de datos en PostgreSQL
createdb contacts_db

# Luego, inicializar el esquema
python scripts/init_db.py

# 4. Ejecutar el bot
python main.py
```

## Verificación

### Health Check

Envía `/health` al bot para verificar el estado de todos los servicios.

### Logs

Ver logs en tiempo real:

```bash
# Con Docker
docker-compose logs -f bot

# Local
tail -f logs/app.log
```

### Base de Datos

Verificar que los contactos se guardan:

```bash
# Con Docker
docker-compose exec db psql -U postgres -d contacts_db -c "SELECT * FROM contacts;"

# Local
psql contacts_db -c "SELECT * FROM contacts;"
```

## Troubleshooting

### "Bot no responde"

1. Verificar que el bot está corriendo:
   ```bash
   docker-compose ps
   ```

2. Ver logs de errores:
   ```bash
   docker-compose logs bot | grep -i error
   ```

3. Verificar token:
   ```bash
   curl https://api.telegram.org/bot<TU_TOKEN>/getMe
   ```

### "Error de base de datos"

1. Verificar que PostgreSQL está corriendo:
   ```bash
   docker-compose ps db
   ```

2. Probar conexión:
   ```bash
   docker-compose exec db psql -U postgres -c "SELECT 1;"
   ```

### "Usuario no autorizado"

1. Verificar tu user ID con @userinfobot
2. Agregarlo a `.env`:
   ```env
   TELEGRAM_ALLOWED_USERS=tu_user_id_aqui
   ```
3. Reiniciar:
   ```bash
   docker-compose restart bot
   ```

## Producción

### Checklist

- [ ] Cambiar contraseñas de PostgreSQL
- [ ] Configurar backups automáticos
- [ ] Habilitar HTTPS si usas webhooks
- [ ] Configurar monitoreo y alertas
- [ ] Revisar límites de rate limiting
- [ ] Configurar reinicio automático
- [ ] Rotar API keys periódicamente

### Docker en Producción

```bash
# Detener servicios
docker-compose down

# Actualizar código
git pull

# Reconstruir y reiniciar
docker-compose up -d --build

# Verificar
docker-compose logs -f bot
```

## Soporte

Si encuentras problemas, revisa:

1. Logs del bot: `docker-compose logs bot`
2. README.md para documentación completa
3. PRD.md para especificaciones técnicas

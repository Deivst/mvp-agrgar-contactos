# Setup Local - Instalación Sin PostgreSQL

## Estado Actual

✅ Python 3.x instalado
✅ Entorno virtual creado (`venv/`)
✅ Archivo `.env` configurado
⏳ Instalando dependencias...

## Pasos Completados

1. **Entorno Virtual** - Ya existe en `./venv/`
2. **Configuración** - `.env` con credenciales de Telegram y Gemini
3. **Dependencias** - Instalándose (excluyendo psycopg2 que requiere PostgreSQL)

## Próximas Opciones

### Opción A: Usar PostgreSQL (Recomendado para Producción)

Si PostgreSQL no está instalado:

1. **Descargar PostgreSQL**: https://www.postgresql.org/download/windows/
2. **Instalar**: Asegurar que se incluye pgAdmin
3. **Crear BD**:
   ```bash
   psql -U postgres
   CREATE DATABASE contacts_db;
   \q
   ```

4. **Instalar psycopg2**:
   ```bash
   .\venv\Scripts\pip install psycopg2-binary
   ```

5. **Inicializar base de datos**:
   ```bash
   .\venv\Scripts\python scripts/init_db.py
   ```

6. **Ejecutar el bot**:
   ```bash
   .\venv\Scripts\python main.py
   ```

### Opción B: Usar SQLite (Para Testing)

Para probar el sistema sin PostgreSQL instalado:

1. **Actualizar `.env`** con SQLite:
   ```env
   DATABASE_URL=sqlite:///./contacts.db
   ```

2. **Instalar dependencias mínimas**:
   ```bash
   .\venv\Scripts\pip install sqlalchemy python-dotenv
   ```

3. **Ejecutar el bot** (creará la BD automáticamente):
   ```bash
   .\venv\Scripts\python main.py
   ```

## Verificar Instalación

```bash
# Activar el entorno virtual
.\venv\Scripts\activate

# Verificar dependencias instaladas
pip list | findstr telegram
pip list | findstr google-generative
```

## Logs

Los logs se guardarán en:
- Consola: Salida en tiempo real
- Archivo: `logs/app.log` (formato JSON)

## Variables de Entorno Críticas

Verificar que `.env` contiene:
- `TELEGRAM_BOT_TOKEN` - Token válido de Telegram
- `TELEGRAM_ALLOWED_USERS` - Tu user ID
- `GEMINI_API_KEY` - API key válido de Google Gemini
- `DATABASE_URL` - PostgreSQL o SQLite

## Troubleshooting

### "ModuleNotFoundError: No module named 'psycopg2'"

**Solución**: Usa SQLite (`sqlite:///./contacts.db`) o instala PostgreSQL

### "Error: pg_config executable not found"

**Solución**: Instala PostgreSQL completo desde https://www.postgresql.org/download/

### Bot no responde

1. Verifica el `.env` tiene credenciales válidas
2. Revisa `logs/app.log` para errores
3. Confirma que tienes conexión a internet (para Telegram y Gemini APIs)

## Estructura de Directorios

```
mvp-agrgar-contactos/
├── venv/                          # Entorno virtual
├── .env                           # Variables de entorno (credenciales)
├── .env.example                   # Plantilla de .env
├── main.py                        # Punto de entrada del bot
├── config/
│   └── settings.py               # Configuración de la app
├── src/
│   ├── agents/                   # Agentes del sistema
│   ├── services/                 # Servicios externos
│   ├── validators/               # Validadores
│   ├── models/                   # Modelos de datos
│   └── utils/                    # Utilidades
├── scripts/
│   ├── init_db.py               # Inicializar BD (requiere PostgreSQL)
│   └── init_db.sql              # Script SQL directo
├── logs/                         # Logs de la aplicación
└── contacts.db                  # Base de datos SQLite (si se usa)
```

## Siguientes Pasos

1. **Esperarar** a que termine la instalación de dependencias
2. **Inicializar base de datos** (ver Opción A o B arriba)
3. **Ejecutar**: `.\venv\Scripts\python main.py`
4. **Probar** en Telegram enviando un mensaje al bot

---

**Nota**: El bot requiere una conexión activa a:
- Telegram Bot API (para recibir/enviar mensajes)
- Google Gemini API (para procesar lenguaje natural)
- Base de datos (PostgreSQL o SQLite)

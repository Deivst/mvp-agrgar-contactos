# Sistema Multi-Agente de Gestión de Contactos

Sistema automatizado para registro de contactos mediante Telegram Bot con procesamiento inteligente usando Google Gemini y persistencia en PostgreSQL.

## Características

- Registro de contactos mediante mensajes de Telegram en lenguaje natural
- Extracción automática de entidades con Google Gemini (nombre, teléfono, referido)
- Persistencia en PostgreSQL con SQLAlchemy ORM
- Envío de contactos mediante:
  - Archivo vCard (.vcf) para importación automática
  - Botón inline de Telegram para agregar directamente
- Sistema de seguridad con whitelist de usuarios
- Rate limiting configurable
- Logging estructurado en JSON
- Dockerizado y listo para producción

## Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                    USUARIO (Telegram)                   │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│               AGENTE DE SEGURIDAD                       │
│  • Autenticación (whitelist)                            │
│  • Rate limiting                                        │
│  • Validación de mensajes                              │
│  • Sanitización de datos                               │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              GOOGLE GEMINI API                          │
│  • Procesamiento de lenguaje natural                   │
│  • Extracción de entidades                             │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│           AGENTE DE PERSISTENCIA                        │
│  • Guardado en PostgreSQL                              │
│  • Generación de vCard                                 │
│  • Notificación con botón Telegram                     │
└─────────────────────────┬───────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│              POSTGRESQL DATABASE                        │
└─────────────────────────────────────────────────────────┘
```

## Requisitos Previos

### Opción 1: Instalación Local

- Python 3.10 o superior
- PostgreSQL 12 o superior
- Cuenta de Telegram y bot creado (@BotFather)
- API key de Google Gemini

### Opción 2: Docker (Recomendado)

- Docker 20.10 o superior
- Docker Compose 2.0 o superior

## Instalación

### Opción 1: Instalación Local

#### 1. Clonar el repositorio

```bash
cd agente_identificador_contactos_mvp
```

#### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
.\venv\Scripts\activate  # Windows
```

#### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

#### 4. Configurar variables de entorno

```bash
cp .env.example .env
```

Editar `.env` con tus credenciales:

```env
# Telegram
TELEGRAM_BOT_TOKEN=tu_bot_token_aquí
TELEGRAM_ALLOWED_USERS=123456789,987654321

# Google Gemini
GEMINI_API_KEY=tu_gemini_api_key_aquí

# PostgreSQL
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/contacts_db
```

#### 5. Crear base de datos

```bash
# Opción A: Usando script Python
python scripts/init_db.py

# Opción B: Usando psql
psql -U postgres -f scripts/init_db.sql
```

#### 6. Ejecutar el bot

```bash
python main.py
```

### Opción 2: Docker (Recomendado)

#### 1. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus credenciales
```

#### 2. Levantar servicios con Docker Compose

```bash
# Solo bot y base de datos
docker-compose up -d

# Con pgAdmin (para gestión visual de BD)
docker-compose --profile admin up -d
```

#### 3. Ver logs

```bash
# Logs del bot
docker-compose logs -f bot

# Logs de todos los servicios
docker-compose logs -f
```

#### 4. Detener servicios

```bash
docker-compose down
```

## Configuración

### Obtener credenciales

#### Bot de Telegram

1. Busca @BotFather en Telegram
2. Envía `/newbot` y sigue las instrucciones
3. Copia el token que te proporciona
4. Para obtener tu user ID, envía un mensaje a @userinfobot

#### Google Gemini API

1. Ve a https://ai.google.dev/
2. Crea una API key
3. Copia la key generada

### Variables de entorno

Todas las variables están documentadas en `.env.example`:

| Variable | Descripción | Requerido |
|----------|-------------|-----------|
| `TELEGRAM_BOT_TOKEN` | Token del bot de Telegram | Sí |
| `TELEGRAM_ALLOWED_USERS` | IDs autorizados (separados por coma) | Sí |
| `GEMINI_API_KEY` | API key de Google Gemini | Sí |
| `DATABASE_URL` | URL de conexión a PostgreSQL | Sí |
| `RATE_LIMIT_REQUESTS` | Requests por ventana de tiempo | No (default: 10) |
| `RATE_LIMIT_WINDOW` | Ventana en segundos | No (default: 60) |
| `LOG_LEVEL` | Nivel de logging | No (default: INFO) |

## Uso

### Comandos del Bot

| Comando | Descripción |
|---------|-------------|
| `/start` | Mensaje de bienvenida |
| `/help` | Ayuda y ejemplos |
| `/health` | Estado del sistema (solo usuarios autorizados) |

### Agregar un contacto

Envía un mensaje con la información del contacto. El formato puede ser flexible:

**Ejemplo 1 (Formal):**
```
Juan Carlos Pérez García
300 123 4567
Recomendado por María López Rodríguez
```

**Ejemplo 2 (Informal):**
```
Juan 3001234567 ref María
```

**Ejemplo 3 (Natural):**
```
Me pasaron el contacto de Ana Rodríguez, su número es 315-789-4561, me lo dio Carlos
```

### Respuesta del sistema

El bot responderá con:

1. Mensaje de confirmación con los datos guardados
2. Archivo vCard (.vcf) que puedes tocar para agregar a tus contactos
3. Botón inline "Agregar a Contactos" para agregar directamente desde Telegram

## Desarrollo

### Estructura del Proyecto

```
agente-contactos/
├── src/
│   ├── agents/           # Agentes del sistema
│   │   ├── security_agent.py
│   │   └── persistence_agent.py
│   ├── services/         # Servicios externos
│   │   ├── gemini_service.py
│   │   ├── contacts_api.py
│   │   └── telegram_service.py
│   ├── validators/       # Validadores de datos
│   │   ├── message_validator.py
│   │   └── contact_validator.py
│   ├── models/          # Modelos de datos
│   │   └── contact.py
│   └── utils/           # Utilidades
│       ├── logger.py
│       ├── rate_limiter.py
│       └── helpers.py
├── config/              # Configuración
│   └── settings.py
├── tests/              # Tests
│   ├── unit/
│   └── integration/
├── scripts/            # Scripts auxiliares
│   ├── init_db.sql
│   └── init_db.py
├── main.py            # Punto de entrada
└── docker-compose.yml # Configuración Docker
```

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Tests unitarios
pytest tests/unit/

# Con cobertura
pytest --cov=src --cov-report=html

# Test específico
pytest tests/unit/test_models.py -v
```

### Linting y Formateo

```bash
# Formatear código
black src/ tests/

# Verificar estilo
flake8 src/ tests/

# Type checking
mypy src/
```

## Base de Datos

### Esquema

```sql
CREATE TABLE contacts (
    id VARCHAR(36) PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    quien_lo_recomendo VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    source VARCHAR(50) DEFAULT 'telegram',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Acceder a PostgreSQL

Con Docker:
```bash
# Conectar a PostgreSQL
docker-compose exec db psql -U postgres -d contacts_db

# Consultar contactos
SELECT * FROM contacts ORDER BY created_at DESC LIMIT 10;
```

Con pgAdmin:
1. Acceder a http://localhost:5050
2. Login: admin@admin.com / admin
3. Conectar al servidor: db / postgres / postgres

## Seguridad

### Funcionalidades implementadas

- Whitelist de usuarios autorizados
- Rate limiting (10 requests/minuto por usuario)
- Sanitización de inputs (prevención de inyección)
- Logging de intentos de acceso no autorizado
- Bloqueo automático después de múltiples intentos fallidos
- Variables de entorno para credenciales
- Usuario no-root en Docker

### Agregar usuario autorizado

Editar `.env`:
```env
TELEGRAM_ALLOWED_USERS=123456789,987654321,nuevo_user_id
```

Reiniciar el bot.

## Monitoreo

### Logs

Logs estructurados en formato JSON:

```bash
# Ver logs en tiempo real
tail -f logs/app.log

# Filtrar logs de seguridad
grep "security" logs/app.log

# Ver errores
grep "error" logs/app.log
```

### Métricas

El bot registra:
- Mensajes procesados
- Tasa de éxito/error
- Intentos de acceso no autorizado
- Rate limiting events
- Latencia de Gemini
- Latencia de base de datos

## Troubleshooting

### El bot no responde

1. Verificar que el bot está corriendo:
   ```bash
   docker-compose ps
   # o
   ps aux | grep python
   ```

2. Verificar logs:
   ```bash
   docker-compose logs bot
   ```

3. Verificar token de Telegram:
   ```bash
   curl https://api.telegram.org/bot<TOKEN>/getMe
   ```

### Error de conexión a base de datos

1. Verificar que PostgreSQL está corriendo:
   ```bash
   docker-compose ps db
   ```

2. Verificar credenciales en `.env`

3. Probar conexión manual:
   ```bash
   psql postgresql://postgres:postgres@localhost:5432/contacts_db
   ```

### Gemini API no responde

1. Verificar API key en `.env`
2. Verificar cuota de Gemini API
3. Ver logs de errores de Gemini

### Usuario no autorizado

1. Obtener tu user ID con @userinfobot
2. Agregarlo a `TELEGRAM_ALLOWED_USERS` en `.env`
3. Reiniciar el bot

## Producción

### Checklist de despliegue

- [ ] Variables de entorno configuradas
- [ ] Base de datos PostgreSQL en producción
- [ ] Backups de base de datos configurados
- [ ] Rate limits ajustados según carga esperada
- [ ] Logs centralizados configurados
- [ ] Monitoreo y alertas configuradas
- [ ] SSL/TLS habilitado
- [ ] Reinicio automático configurado
- [ ] Health checks configurados

### Recomendaciones

- Usar PostgreSQL gestionado (AWS RDS, Google Cloud SQL, etc.)
- Implementar backups automáticos
- Configurar alertas de errores
- Escalar horizontalmente si es necesario
- Rotar API keys periódicamente
- Monitorear costos de Gemini API

## API

### Endpoints internos

El sistema expone los siguientes servicios internos:

#### ContactsAPIClient

```python
# Guardar contacto
await contacts_client.save_contact(contact)

# Obtener contacto
contact = await contacts_client.get_contact(contact_id)

# Health check
is_healthy = await contacts_client.health_check()
```

#### GeminiService

```python
# Extraer información
result = await gemini_service.extract_contact_info(message_text)
```

## Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature
3. Asegúrate de que los tests pasen
4. Envía un pull request

## Licencia

Este proyecto está bajo la licencia MIT.

## Soporte

Para reportar bugs o solicitar features, abre un issue en el repositorio.

## Autor

Desarrollado siguiendo las especificaciones del PRD v1.0.

---

**Versión:** 1.0.0
**Última actualización:** Diciembre 2025

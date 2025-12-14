# PRD & SRS: Sistema Multi-Agente de Gestión de Contactos

**Versión:** 1.0  
**Fecha:** Diciembre 2025  
**Autor:** Equipo de Desarrollo  
**Estado:** Borrador

---

## Tabla de Contenidos

1. [Introducción](#1-introducción)
2. [Visión General del Producto](#2-visión-general-del-producto)
3. [Objetivos y Alcance](#3-objetivos-y-alcance)
4. [Stakeholders](#4-stakeholders)
5. [Requerimientos Funcionales](#5-requerimientos-funcionales)
6. [Requerimientos No Funcionales](#6-requerimientos-no-funcionales)
7. [Arquitectura del Sistema](#7-arquitectura-del-sistema)
8. [Especificaciones Técnicas](#8-especificaciones-técnicas)
9. [Interfaces del Sistema](#9-interfaces-del-sistema)
10. [Modelo de Datos](#10-modelo-de-datos)
11. [Casos de Uso](#11-casos-de-uso)
12. [Diagramas de Secuencia](#12-diagramas-de-secuencia)
13. [Seguridad](#13-seguridad)
14. [Plan de Pruebas](#14-plan-de-pruebas)
15. [Riesgos y Mitigaciones](#15-riesgos-y-mitigaciones)
16. [Cronograma](#16-cronograma)
17. [Métricas de Éxito](#17-métricas-de-éxito)
18. [Glosario](#18-glosario)
19. [Apéndices](#19-apéndices)

---

## 1. Introducción

### 1.1 Propósito del Documento

Este documento combina el Product Requirements Document (PRD) y el Software Requirements Specification (SRS) para el Sistema Multi-Agente de Gestión de Contactos. Define los requerimientos del producto, especificaciones técnicas y criterios de aceptación para el desarrollo e implementación del sistema.

### 1.2 Alcance del Documento

El documento cubre:
- Definición del problema y solución propuesta
- Requerimientos funcionales y no funcionales
- Arquitectura técnica y especificaciones
- Interfaces, modelos de datos y flujos de proceso
- Criterios de seguridad y pruebas

### 1.3 Definiciones y Acrónimos

| Término | Definición |
|---------|------------|
| PRD | Product Requirements Document |
| SRS | Software Requirements Specification |
| API | Application Programming Interface |
| LLM | Large Language Model |
| JSON | JavaScript Object Notation |
| REST | Representational State Transfer |

### 1.4 Referencias

- Documentación de Google Gemini API
- Documentación de Telegram Bot API
- Estándares de seguridad OWASP

---

## 2. Visión General del Producto

### 2.1 Descripción del Producto

El Sistema Multi-Agente de Gestión de Contactos es una solución automatizada que permite registrar nuevos contactos en una libreta digital a través de mensajes de Telegram. El sistema utiliza inteligencia artificial (Google Gemini) para procesar mensajes en lenguaje natural y extraer información estructurada de contactos.

### 2.2 Problema que Resuelve

| Problema Actual | Solución Propuesta |
|-----------------|-------------------|
| Registro manual de contactos consume tiempo | Automatización mediante mensajes de Telegram |
| Pérdida de información sobre quién refirió el contacto | Trazabilidad completa de referidos |
| Formatos inconsistentes en el registro | Estructuración automática con IA |
| Falta de validación de datos | Validación en múltiples capas |
| Sin control de acceso | Sistema de autenticación por usuario |

### 2.3 Propuesta de Valor

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROPUESTA DE VALOR                           │
├─────────────────────────────────────────────────────────────────┤
│  ✓ Registro de contactos en segundos vía Telegram              │
│  ✓ Procesamiento inteligente de lenguaje natural               │
│  ✓ Trazabilidad completa de quién refirió cada contacto        │
│  ✓ Seguridad y control de acceso                               │
│  ✓ Integración con sistemas existentes vía API                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. Objetivos y Alcance

### 3.1 Objetivos del Producto

#### Objetivos Primarios

| ID | Objetivo | Métrica de Éxito |
|----|----------|------------------|
| OBJ-01 | Automatizar el registro de contactos | Reducir tiempo de registro en 80% |
| OBJ-02 | Garantizar trazabilidad de referidos | 100% de contactos con campo de referencia |
| OBJ-03 | Asegurar integridad de datos | Tasa de error < 2% |
| OBJ-04 | Controlar acceso al sistema | 0 accesos no autorizados |

#### Objetivos Secundarios

| ID | Objetivo | Métrica de Éxito |
|----|----------|------------------|
| OBJ-05 | Proveer experiencia de usuario fluida | Tiempo de respuesta < 3 segundos |
| OBJ-06 | Facilitar integración con otros sistemas | API REST documentada |
| OBJ-07 | Mantener registro de auditoría | Logs de todas las operaciones |

### 3.2 Alcance del Proyecto

#### Dentro del Alcance (In Scope)

- Recepción de mensajes de Telegram
- Validación de usuarios autorizados
- Procesamiento de mensajes con Google Gemini
- Extracción de: nombre, teléfono, referido
- Estructuración en formato JSON
- Persistencia en libreta de contactos vía API REST
- Notificación de resultado al usuario
- Logging y trazabilidad

#### Fuera del Alcance (Out of Scope)

- Interfaz web de administración
- Edición o eliminación de contactos vía Telegram
- Soporte para imágenes o archivos adjuntos
- Integración con CRM externos
- Reportes y analítica
- Aplicación móvil nativa

### 3.3 Supuestos y Dependencias

#### Supuestos

1. Los usuarios tienen acceso a Telegram
2. La API de la libreta de contactos está disponible
3. Google Gemini API tiene disponibilidad > 99%
4. Los mensajes contienen información mínima requerida

#### Dependencias

| Dependencia | Tipo | Criticidad |
|-------------|------|------------|
| Telegram Bot API | Externa | Alta |
| Google Gemini API | Externa | Alta |
| API Libreta de Contactos | Interna | Alta |
| Servidor de hosting | Infraestructura | Alta |

---

## 4. Stakeholders

### 4.1 Identificación de Stakeholders

| Rol | Responsabilidad | Interés Principal |
|-----|-----------------|-------------------|
| Product Owner | Definición de requerimientos | Valor de negocio |
| Usuarios Finales | Uso del sistema | Facilidad de uso |
| Equipo de Desarrollo | Implementación | Claridad técnica |
| Equipo de QA | Validación | Criterios de aceptación |
| Administrador de Sistemas | Operación | Mantenibilidad |
| Oficial de Seguridad | Cumplimiento | Protección de datos |

### 4.2 Matriz de Comunicación

| Stakeholder | Información | Frecuencia | Canal |
|-------------|-------------|------------|-------|
| Product Owner | Estado del proyecto | Semanal | Reunión |
| Equipo Desarrollo | Especificaciones técnicas | Continuo | Documentación |
| Usuarios | Guías de uso | Al desplegar | Telegram |

---

## 5. Requerimientos Funcionales

### 5.1 Módulo: Recepción de Mensajes (RF-100)

| ID | Requerimiento | Prioridad | Criterio de Aceptación |
|----|---------------|-----------|------------------------|
| RF-101 | El sistema debe recibir mensajes de texto de Telegram | Alta | Mensaje recibido en < 1 segundo |
| RF-102 | El sistema debe identificar el usuario que envía el mensaje | Alta | ID de usuario extraído correctamente |
| RF-103 | El sistema debe registrar timestamp de recepción | Media | Timestamp en formato ISO 8601 |
| RF-104 | El sistema debe soportar mensajes en español | Alta | Procesamiento correcto de caracteres especiales |

### 5.2 Módulo: Agente de Seguridad (RF-200)

| ID | Requerimiento | Prioridad | Criterio de Aceptación |
|----|---------------|-----------|------------------------|
| RF-201 | El sistema debe validar que el usuario está autorizado | Alta | Solo usuarios en whitelist pueden operar |
| RF-202 | El sistema debe rechazar mensajes de usuarios no autorizados | Alta | Mensaje de error enviado al usuario |
| RF-203 | El sistema debe validar formato mínimo del mensaje | Alta | Mensajes < 5 caracteres rechazados |
| RF-204 | El sistema debe sanitizar datos de entrada | Alta | Caracteres peligrosos removidos |
| RF-205 | El sistema debe implementar rate limiting | Media | Máximo 10 mensajes por minuto por usuario |
| RF-206 | El sistema debe registrar intentos de acceso no autorizado | Alta | Log con IP, timestamp, user_id |

### 5.3 Módulo: Procesamiento con Gemini (RF-300)

| ID | Requerimiento | Prioridad | Criterio de Aceptación |
|----|---------------|-----------|------------------------|
| RF-301 | El sistema debe enviar el mensaje a Google Gemini para procesamiento | Alta | Request enviado correctamente |
| RF-302 | El sistema debe extraer el nombre del contacto | Alta | Nombre extraído con precisión > 95% |
| RF-303 | El sistema debe extraer el número de teléfono | Alta | Teléfono normalizado correctamente |
| RF-304 | El sistema debe extraer el nombre del referido | Alta | Referido identificado correctamente |
| RF-305 | El sistema debe manejar errores de Gemini API | Alta | Fallback o mensaje de error apropiado |
| RF-306 | El sistema debe estructurar la respuesta en JSON | Alta | JSON válido según esquema definido |

### 5.4 Módulo: Validación de Datos (RF-400)

| ID | Requerimiento | Prioridad | Criterio de Aceptación |
|----|---------------|-----------|------------------------|
| RF-401 | El sistema debe validar que el nombre no esté vacío | Alta | Error si nombre es vacío |
| RF-402 | El sistema debe validar formato de teléfono | Alta | Teléfono con 10-15 dígitos |
| RF-403 | El sistema debe validar que el referido no esté vacío | Media | Advertencia si referido está vacío |
| RF-404 | El sistema debe normalizar el número de teléfono | Alta | Formato: +[código país][número] |

### 5.5 Módulo: Persistencia (RF-500)

| ID | Requerimiento | Prioridad | Criterio de Aceptación |
|----|---------------|-----------|------------------------|
| RF-501 | El sistema debe enviar POST a la API de contactos | Alta | Request HTTP 201 Created |
| RF-502 | El sistema debe manejar errores de la API de contactos | Alta | Reintentos y mensaje de error |
| RF-503 | El sistema debe confirmar el guardado exitoso | Alta | ID de contacto retornado |
| RF-504 | El sistema debe registrar la operación en logs | Media | Log con todos los detalles |

### 5.6 Módulo: Notificaciones (RF-600)

| ID | Requerimiento | Prioridad | Criterio de Aceptación |
|----|---------------|-----------|------------------------|
| RF-601 | El sistema debe notificar éxito al usuario | Alta | Mensaje con datos del contacto guardado |
| RF-602 | El sistema debe notificar errores al usuario | Alta | Mensaje descriptivo del error |
| RF-603 | El sistema debe incluir resumen del contacto guardado | Media | Nombre, teléfono, referido mostrados |

---

## 6. Requerimientos No Funcionales

### 6.1 Rendimiento (RNF-100)

| ID | Requerimiento | Especificación |
|----|---------------|----------------|
| RNF-101 | Tiempo de respuesta end-to-end | < 5 segundos (P95) |
| RNF-102 | Tiempo de procesamiento Gemini | < 3 segundos |
| RNF-103 | Throughput del sistema | 100 mensajes/minuto |
| RNF-104 | Concurrencia | 50 usuarios simultáneos |

### 6.2 Disponibilidad (RNF-200)

| ID | Requerimiento | Especificación |
|----|---------------|----------------|
| RNF-201 | Uptime del sistema | 99.5% mensual |
| RNF-202 | Tiempo máximo de downtime | 4 horas/mes |
| RNF-203 | Recovery Time Objective (RTO) | < 1 hora |
| RNF-204 | Recovery Point Objective (RPO) | < 5 minutos |

### 6.3 Seguridad (RNF-300)

| ID | Requerimiento | Especificación |
|----|---------------|----------------|
| RNF-301 | Autenticación de usuarios | Whitelist de IDs de Telegram |
| RNF-302 | Encriptación en tránsito | TLS 1.3 |
| RNF-303 | Almacenamiento de credenciales | Variables de entorno / Vault |
| RNF-304 | Sanitización de inputs | OWASP guidelines |
| RNF-305 | Rate limiting | 10 requests/minuto/usuario |
| RNF-306 | Logging de seguridad | Todos los accesos registrados |

### 6.4 Escalabilidad (RNF-400)

| ID | Requerimiento | Especificación |
|----|---------------|----------------|
| RNF-401 | Escalamiento horizontal | Soporte para múltiples instancias |
| RNF-402 | Crecimiento de usuarios | Hasta 1000 usuarios autorizados |
| RNF-403 | Volumen de datos | 10,000 contactos/mes |

### 6.5 Mantenibilidad (RNF-500)

| ID | Requerimiento | Especificación |
|----|---------------|----------------|
| RNF-501 | Cobertura de código | > 80% |
| RNF-502 | Documentación de código | Docstrings en todas las funciones |
| RNF-503 | Logging estructurado | Formato JSON |
| RNF-504 | Versionamiento | Semantic versioning |

### 6.6 Compatibilidad (RNF-600)

| ID | Requerimiento | Especificación |
|----|---------------|----------------|
| RNF-601 | Python version | 3.10+ |
| RNF-602 | Telegram Bot API | v6.0+ |
| RNF-603 | Google Gemini API | gemini-1.5-flash |

---

## 7. Arquitectura del Sistema

### 7.1 Diagrama de Arquitectura de Alto Nivel

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              SISTEMA MULTI-AGENTE                               │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│   ┌───────────────┐                                                             │
│   │   TELEGRAM    │                                                             │
│   │   CLOUD API   │                                                             │
│   └───────┬───────┘                                                             │
│           │ Webhook/Polling                                                     │
│           ▼                                                                     │
│   ┌───────────────────────────────────────────────────────────────────────┐    │
│   │                         CAPA DE ENTRADA                               │    │
│   │   ┌─────────────────────────────────────────────────────────────┐     │    │
│   │   │                   Telegram Bot Handler                       │     │    │
│   │   │   • Recepción de mensajes                                   │     │    │
│   │   │   • Extracción de metadata (user_id, chat_id, timestamp)    │     │    │
│   │   └─────────────────────────────────────────────────────────────┘     │    │
│   └───────────────────────────────────────────────────────────────────────┘    │
│                                       │                                         │
│                                       ▼                                         │
│   ┌───────────────────────────────────────────────────────────────────────┐    │
│   │                      AGENTE DE SEGURIDAD                              │    │
│   │   ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐      │    │
│   │   │  Autenticación  │  │   Validación    │  │  Sanitización   │      │    │
│   │   │  de Usuario     │  │   de Formato    │  │   de Datos      │      │    │
│   │   └─────────────────┘  └─────────────────┘  └─────────────────┘      │    │
│   │   ┌─────────────────┐  ┌─────────────────┐                           │    │
│   │   │  Rate Limiting  │  │    Logging      │                           │    │
│   │   └─────────────────┘  └─────────────────┘                           │    │
│   └───────────────────────────────────────────────────────────────────────┘    │
│                                       │                                         │
│                                       ▼                                         │
│   ┌───────────────────────────────────────────────────────────────────────┐    │
│   │                      CAPA DE PROCESAMIENTO                            │    │
│   │   ┌─────────────────────────────────────────────────────────────┐     │    │
│   │   │                   GOOGLE GEMINI API                          │     │    │
│   │   │   • Procesamiento de lenguaje natural                       │     │    │
│   │   │   • Extracción de entidades                                 │     │    │
│   │   │   • Estructuración JSON                                     │     │    │
│   │   └─────────────────────────────────────────────────────────────┘     │    │
│   │   ┌─────────────────────────────────────────────────────────────┐     │    │
│   │   │                   Validador de Datos                         │     │    │
│   │   │   • Validación de campos requeridos                         │     │    │
│   │   │   • Normalización de teléfono                               │     │    │
│   │   └─────────────────────────────────────────────────────────────┘     │    │
│   └───────────────────────────────────────────────────────────────────────┘    │
│                                       │                                         │
│                                       ▼                                         │
│   ┌───────────────────────────────────────────────────────────────────────┐    │
│   │                      AGENTE DE PERSISTENCIA                           │    │
│   │   ┌─────────────────────────────────────────────────────────────┐     │    │
│   │   │                   HTTP Client                                │     │    │
│   │   │   • POST /contacts                                          │     │    │
│   │   │   • Manejo de errores y reintentos                          │     │    │
│   │   │   • Confirmación de operación                               │     │    │
│   │   └─────────────────────────────────────────────────────────────┘     │    │
│   └───────────────────────────────────────────────────────────────────────┘    │
│                                       │                                         │
│                                       ▼                                         │
│   ┌───────────────────────────────────────────────────────────────────────┐    │
│   │                      CAPA DE NOTIFICACIÓN                             │    │
│   │   • Envío de confirmación al usuario                                  │    │
│   │   • Notificación de errores                                           │    │
│   └───────────────────────────────────────────────────────────────────────┘    │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
                         ┌──────────────────────────┐
                         │   LIBRETA DE CONTACTOS   │
                         │        (API REST)        │
                         │   POST /api/v1/contacts  │
                         └──────────────────────────┘
```

### 7.2 Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              COMPONENTES                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                           main.py                                    │   │
│  │                     ContactsOrchestrator                             │   │
│  │  ┌─────────────────────────────────────────────────────────────┐    │   │
│  │  │  + handle_telegram_message(update, context)                  │    │   │
│  │  │  + security_agent: SecurityAgent                             │    │   │
│  │  │  + persistence_agent: PersistenceAgent                       │    │   │
│  │  └─────────────────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│              ┌─────────────────────┼─────────────────────┐                 │
│              │                     │                     │                 │
│              ▼                     ▼                     ▼                 │
│  ┌───────────────────┐  ┌───────────────────┐  ┌───────────────────┐      │
│  │  SecurityAgent    │  │ PersistenceAgent  │  │   GeminiService   │      │
│  │                   │  │                   │  │                   │      │
│  │ +process_request()│  │ +save_contact()   │  │ +extract_contact_ │      │
│  │ +validate_origin()│  │                   │  │  info()           │      │
│  │ +validate_format()│  │                   │  │ +normalize_phone()│      │
│  │ +sanitize_data()  │  │                   │  │                   │      │
│  └───────────────────┘  └───────────────────┘  └───────────────────┘      │
│              │                     │                     │                 │
│              │                     │                     │                 │
│              ▼                     ▼                     ▼                 │
│  ┌───────────────────────────────────────────────────────────────────┐    │
│  │                           models/                                  │    │
│  │  ┌─────────────────────────────────────────────────────────────┐  │    │
│  │  │                        Contact                               │  │    │
│  │  │  + nombre: str                                               │  │    │
│  │  │  + telefono: str                                             │  │    │
│  │  │  + quien_lo_recomendo: str                                   │  │    │
│  │  │  + timestamp: datetime                                       │  │    │
│  │  │  + source: str                                               │  │    │
│  │  └─────────────────────────────────────────────────────────────┘  │    │
│  └───────────────────────────────────────────────────────────────────┘    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 7.3 Estructura de Directorios

```
agente-contactos/
│
├── src/
│   ├── __init__.py
│   │
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── security_agent.py       # Agente principal de seguridad
│   │   └── persistence_agent.py    # Agente de persistencia
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── telegram_service.py     # Integración con Telegram
│   │   ├── gemini_service.py       # Cliente Google Gemini API
│   │   └── contacts_api.py         # Cliente API libreta contactos
│   │
│   ├── validators/
│   │   ├── __init__.py
│   │   ├── message_validator.py    # Validación de mensajes
│   │   └── contact_validator.py    # Validación de datos de contacto
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── contact.py              # Modelo de datos Contact
│   │
│   └── utils/
│       ├── __init__.py
│       ├── logger.py               # Configuración de logging
│       └── helpers.py              # Funciones auxiliares
│
├── tests/
│   ├── __init__.py
│   ├── test_security_agent.py
│   ├── test_persistence_agent.py
│   ├── test_gemini_service.py
│   └── test_validators.py
│
├── config/
│   ├── __init__.py
│   └── settings.py                 # Configuración centralizada
│
├── docs/
│   ├── api.md
│   └── deployment.md
│
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── main.py                         # Punto de entrada
```

---

## 8. Especificaciones Técnicas

### 8.1 Stack Tecnológico

| Capa | Tecnología | Versión | Justificación |
|------|------------|---------|---------------|
| Lenguaje | Python | 3.10+ | Ecosistema maduro para IA |
| Bot Framework | python-telegram-bot | 21.0 | Oficial y bien mantenido |
| IA/LLM | Google Gemini | 1.5-flash | Balance costo/rendimiento |
| HTTP Client | httpx | 0.27.0 | Async nativo |
| Validación | Pydantic | 2.6.0 | Type hints y validación |
| Configuración | python-dotenv | 1.0.0 | Manejo de variables de entorno |

### 8.2 APIs Externas

#### 8.2.1 Telegram Bot API

```yaml
Endpoint Base: https://api.telegram.org/bot{token}/
Métodos Utilizados:
  - getUpdates (polling)
  - sendMessage
  - getMe
Autenticación: Bot Token
Rate Limits: 30 mensajes/segundo
```

#### 8.2.2 Google Gemini API

```yaml
Endpoint Base: https://generativelanguage.googleapis.com/
Modelo: gemini-1.5-flash
Autenticación: API Key
Rate Limits: 60 requests/minuto (free tier)
Timeout Recomendado: 30 segundos
```

#### 8.2.3 API Libreta de Contactos

```yaml
Endpoint Base: https://api.libreta-contactos.com/v1/
Métodos:
  POST /contacts:
    Request:
      Content-Type: application/json
      Authorization: Bearer {api_key}
      Body:
        {
          "nombre": "string",
          "telefono": "string",
          "quien_lo_recomendo": "string",
          "timestamp": "ISO 8601",
          "source": "string"
        }
    Response:
      201 Created:
        {
          "id": "uuid",
          "created_at": "ISO 8601"
        }
      400 Bad Request:
        {
          "error": "string",
          "details": {}
        }
      401 Unauthorized:
        {
          "error": "Invalid API key"
        }
```

### 8.3 Configuración del Sistema

```python
# config/settings.py

from pydantic_settings import BaseSettings
from typing import List, Optional

class Settings(BaseSettings):
    # Telegram
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_ALLOWED_USERS: List[int] = []
    
    # Google Gemini
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-1.5-flash"
    GEMINI_TIMEOUT: int = 30
    
    # API Contactos
    CONTACTS_API_URL: str
    CONTACTS_API_KEY: str
    CONTACTS_API_TIMEOUT: int = 10
    
    # Seguridad
    RATE_LIMIT_REQUESTS: int = 10
    RATE_LIMIT_WINDOW: int = 60  # segundos
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # General
    ENVIRONMENT: str = "development"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

### 8.4 Variables de Entorno

```bash
# .env.example

# ========================================
# TELEGRAM CONFIGURATION
# ========================================
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_ALLOWED_USERS=123456789,987654321

# ========================================
# GOOGLE GEMINI CONFIGURATION
# ========================================
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-1.5-flash
GEMINI_TIMEOUT=30

# ========================================
# CONTACTS API CONFIGURATION
# ========================================
CONTACTS_API_URL=https://api.libreta-contactos.com/v1
CONTACTS_API_KEY=your_contacts_api_key_here
CONTACTS_API_TIMEOUT=10

# ========================================
# SECURITY CONFIGURATION
# ========================================
RATE_LIMIT_REQUESTS=10
RATE_LIMIT_WINDOW=60

# ========================================
# LOGGING CONFIGURATION
# ========================================
LOG_LEVEL=INFO
LOG_FORMAT=json

# ========================================
# GENERAL CONFIGURATION
# ========================================
ENVIRONMENT=development
DEBUG=false
```

---

## 9. Interfaces del Sistema

### 9.1 Interfaz de Usuario (Telegram)

#### 9.1.1 Flujo de Conversación

```
Usuario                                          Bot
   │                                              │
   │  "Juan Pérez 3001234567                      │
   │   recomendado por María"                     │
   │ ─────────────────────────────────────────▶   │
   │                                              │
   │   ✅ Contacto guardado exitosamente:         │
   │                                              │
   │   👤 Nombre: Juan Pérez                      │
   │   📱 Teléfono: +573001234567                 │
   │   🤝 Recomendado por: María                  │
   │ ◀─────────────────────────────────────────   │
   │                                              │
```

#### 9.1.2 Mensajes del Sistema

| Escenario | Mensaje |
|-----------|---------|
| Éxito | ✅ Contacto guardado exitosamente:\n\n👤 Nombre: {nombre}\n📱 Teléfono: {telefono}\n🤝 Recomendado por: {referido} |
| Usuario no autorizado | ❌ No tienes autorización para usar este bot. |
| Mensaje inválido | ❌ El mensaje es muy corto o no contiene información válida. |
| Error de procesamiento | ❌ No pude procesar el mensaje. Por favor, incluye: nombre, teléfono y quién te lo recomendó. |
| Error de API | ❌ Error al guardar el contacto. Por favor, intenta nuevamente. |
| Campos faltantes | ❌ Campos faltantes: {campos}. Por favor, incluye toda la información. |

### 9.2 Interfaz de Programación (API Interna)

#### 9.2.1 SecurityAgent

```python
class SecurityAgent:
    """
    Agente de seguridad para validación y procesamiento de mensajes.
    
    Attributes:
        allowed_users: Lista de IDs de Telegram autorizados
        gemini_service: Servicio de procesamiento con Gemini
    """
    
    async def process_request(self, message: dict) -> dict:
        """
        Procesa una solicitud de mensaje de Telegram.
        
        Args:
            message: Diccionario con keys:
                - text: str - Contenido del mensaje
                - user_id: int - ID del usuario de Telegram
                - chat_id: int - ID del chat
                
        Returns:
            dict: Resultado del procesamiento
                - success: bool
                - contact: dict (si success=True)
                - error: str (si success=False)
        """
        pass
```

#### 9.2.2 PersistenceAgent

```python
class PersistenceAgent:
    """
    Agente de persistencia para guardar contactos en la API externa.
    
    Attributes:
        api_url: URL base de la API de contactos
        api_key: Clave de autenticación
    """
    
    async def save_contact(self, contact: dict) -> dict:
        """
        Guarda un contacto en la libreta.
        
        Args:
            contact: Diccionario con datos del contacto
                - nombre: str
                - telefono: str
                - quien_lo_recomendo: str
                - timestamp: str (ISO 8601)
                - source: str
                
        Returns:
            dict: Resultado de la operación
                - success: bool
                - contact_id: str (si success=True)
                - error: str (si success=False)
        """
        pass
```

#### 9.2.3 GeminiService

```python
class GeminiService:
    """
    Servicio para extracción de entidades usando Google Gemini.
    
    Attributes:
        model: Modelo de Gemini a utilizar
        extraction_prompt: Template del prompt de extracción
    """
    
    async def extract_contact_info(self, message_text: str) -> dict:
        """
        Extrae información de contacto de un mensaje de texto.
        
        Args:
            message_text: Texto del mensaje a procesar
            
        Returns:
            dict: Resultado de la extracción
                - success: bool
                - data: dict con nombre, telefono, quien_lo_recomendo
                - error: str (si success=False)
        """
        pass
```

---

## 10. Modelo de Datos

### 10.1 Diagrama Entidad-Relación

```
┌─────────────────────────────────────────────────────────────────┐
│                           Contact                               │
├─────────────────────────────────────────────────────────────────┤
│  PK  id: UUID                                                   │
│      nombre: VARCHAR(255)                    NOT NULL           │
│      telefono: VARCHAR(20)                   NOT NULL           │
│      quien_lo_recomendo: VARCHAR(255)        NOT NULL           │
│      timestamp: TIMESTAMP                    NOT NULL           │
│      source: VARCHAR(50)                     DEFAULT 'telegram' │
│      created_at: TIMESTAMP                   AUTO               │
│      updated_at: TIMESTAMP                   AUTO               │
└─────────────────────────────────────────────────────────────────┘
```

### 10.2 Esquema JSON

#### 10.2.1 Contact Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Contact",
  "type": "object",
  "required": ["nombre", "telefono", "quien_lo_recomendo"],
  "properties": {
    "nombre": {
      "type": "string",
      "minLength": 1,
      "maxLength": 255,
      "description": "Nombre completo del contacto"
    },
    "telefono": {
      "type": "string",
      "pattern": "^\\+?[0-9]{10,15}$",
      "description": "Número de teléfono normalizado"
    },
    "quien_lo_recomendo": {
      "type": "string",
      "minLength": 1,
      "maxLength": 255,
      "description": "Nombre de quien recomendó el contacto"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "Fecha y hora de registro (ISO 8601)"
    },
    "source": {
      "type": "string",
      "enum": ["telegram", "api", "manual"],
      "default": "telegram",
      "description": "Origen del contacto"
    }
  }
}
```

#### 10.2.2 Ejemplos de Datos

```json
// Ejemplo 1: Contacto completo
{
  "nombre": "Juan Carlos Pérez García",
  "telefono": "+573001234567",
  "quien_lo_recodo": "María López",
  "timestamp": "2025-01-15T10:30:00Z",
  "source": "telegram"
}

// Ejemplo 2: Contacto con formato diferente de teléfono
{
  "nombre": "Ana María Rodríguez",
  "telefono": "+573157894561",
  "quien_lo_recomendo": "Carlos Ruiz Méndez",
  "timestamp": "2025-01-15T14:22:00Z",
  "source": "telegram"
}
```

### 10.3 Modelo Pydantic

```python
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Literal
import re

class Contact(BaseMode  """Modelo de datos para un contacto."""
    
    nombre: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Nombre completo del contacto"
    )
    
    telefono: str = Field(
        ...,
        description="Número de teléfono normalizado"
    )
    
    quien_lo_recomendo: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Nombre de quien recomendó el contacto"
    )
    
    timestamp: datetime = Field(
        defa_factory=datetime.utcnow,
        description="Fecha y hora de registro"
    )
    
    source: Literal["telegram", "api", "manual"] = Field(
        default="telegram",
        description="Origen del contacto"
    )
    
    @field_validator('telefono')
    @classmethod
    def validate_telefono(cls, v: str) -> str:
        """Valida y normaliza el número de teléfono."""
        # Remover caracteres no numéricos excepto +
        cleaned = re.sub(r'[^\d+]', '', v)
        
        # Validar longitud
     digits_only = cleaned.replace('+', '')
        if len(digits_only) < 10 or len(digits_only) > 15:
            raise ValueError('El teléfono debe tener entre 10 y 15 dígitos')
        
        # Agregar código de país si no existe
        if not cleaned.startswith('+'):
            cleaned = '+57' + cleaned
            
        return cleaned
    
    @field_validator('nombre', 'quien_lo_recomendo')
    @classmethod
    def validate_names(cls, v: str) -> str:
        """Limpia y valida nombres."""
    # Remover espacios extras
        cleaned = ' '.join(v.split())
        
        if not cleaned:
            raise ValueError('El campo no puede estar vacío')
            
        return cleaned
    
    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Juan Pérez",
                "telefono": "+573001234567",
                "quien_lo_recomendo": "María López",
                "timestamp": "2025-01-15T10:30:00Z",
                "source": "telegram"
        }
        }
```

---

## 11. Casos de Uso

### 11.1 Diagrama de Casos de Uso

```
                    ┌─────────────────────────────────────────┐
                    │       Sistema de Gestión de Contactos   │
                    └─────────────────────────────────────────┘
                                        │
        ┌─â─────────────────────┼───────────────────────────────┐
        │                               │                               │
        ▼                               ▼                               ▼
┌───────────────┐              ┌───────────────┐              ┌───────────────┐
│  UC-01      │              │    UC-02      │              │    UC-03      │
│   Registrar   │              │   Validar     │              │   Consultar   │
│   Contacto    │              │   Usuario     │              │   Estado      │
└───────────────┘              └───────────────┘              └───────────────┘
        │                               │                   │
        │                               │                               │
        ▼                               ▼                               ▼
┌───────────────┐              ┌───────────────┐              ┌───────────────┐
│               │              │               │              │               │
│    Usuario    │              │    Sistema    │              in      │
│  Autorizado   │              │   (Interno)   │              │               │
│               │              │               │              │               │
└───────────────┘              └───────────────┘              └───────────────┘
```

### 11.2 Descripción de Casos de Uso

#### UC-01: Registrar Contacto

| Campo | Descripción |
|-------|-------------|
| **ID** UC-01 |
| **Nombre** | Registrar Contacto |
| **Actor Principal** | Usuario Autorizado |
| **Descripción** | Permite registrar un nuevo contacto enviando un mensaje de texto por Telegram |
| **Precondiciones** | - Usuario tiene cuenta de Telegram<br>- Usuario está en la lista de autorizados<br>- Bot está activo |
| **Postcondiciones** | - Contacto guardado en la libreta<br>- Usuario recibe confirmación |

**Flujo Principal:**

| Paso | Actor | Sistema |
|------|-------|---------|
| 1 | Envía mensaje coos del contacto | - |
| 2 | - | Valida autorización del usuario |
| 3 | - | Valida formato del mensaje |
| 4 | - | Procesa mensaje con Gemini |
| 5 | - | Extrae: nombre, teléfono, referido |
| 6 | - | Valida campos requeridos |
| 7 | - | Envía POST a API de contactos |
| 8 | - | Envía confirmación al usuario |

**Flujos Alternativos:**

| ID | Condición | Acción |
|----|-----------|--------|
| 2a | Usuario no autorizado | Enviar mensaje de error y terminar |
| 3a | Mensaje muy corto | Enviar mensaje r y terminar |
| 5a | No se pueden extraer datos | Enviar mensaje de error y terminar |
| 6a | Campos faltantes | Enviar mensaje con campos faltantes |
| 7a | Error en API | Reintentar o enviar error |

#### UC-02: Validar Usuario

| Campo | Descripción |
|-------|-------------|
| **ID** | UC-02 |
| **Nombre** | Validar Usuario |
| **Actor Principal** | Sistema (Interno) |
| **Descripción** | Verifica que el usuario que envía el mensaje está autorizado |
| **Precondiciones** | - Mensaje recibido de Tele |
| **Postcondiciones** | - Usuario validado o rechazado |

**Flujo Principal:**

| Paso | Acción |
|------|--------|
| 1 | Extraer user_id del mensaje |
| 2 | Buscar user_id en lista de autorizados |
| 3 | Si existe, permitir continuar |
| 4 | Si no existe, rechazar y registrar intento |

### 11.3 Matriz de Trazabilidad

| Caso de Uso | Requerimientos Funcionales |
|-------------|----------------------------|
| UC-01 | RF-101, RF-301, RF-302, RF-303, RF-304, RF-501, RF-601 |
| UC-02 | RF-201, RF-202, RF-06 |
| UC-03 | RF-504 |

---

## 12. Diagramas de Secuencia

### 12.1 Flujo Principal: Registro Exitoso de Contacto

```
┌──────┐          ┌──────────┐       ┌─────────────┐      ┌────────┐      ┌──────────────┐      ┌──────────┐
│ User │          │ Telegram │       │ Orchestrator│      │Security│      │    Gemini    │      │Persistence│
â     └────┬─────┘       └──────┬──────┘      └───┬────┘      └──────┬───────┘      └─────┬────┘
   │                   │                    │                 │                  │                   │
   │  Envía mensaje    │                    │                 │                  │                   │
   │────────────────           │                 │                  │                   │
   │                   │                    │                 │                  │                   │
   │                   │  Update (message)  │                 │                  │                   │
   │                   │───────────────────▶│                 │                  │                   │
   │                   │                    â       │                  │                   │
   │                   │                    │ process_request │                  │                   │
   │                   │                    │────────────────▶│                  │                   │
   │                   │                    │                 │                  │                   │
   │                   │                    │                 │ validorigin  │                   │
   │                   │                    │                 │─────────┐        │                   │
   │                   │                    │                 │         │        │                   │
   │                   │                    │                 │◀────────┘        │                   │
   │                   │                    │                 │                  â       │
   │                   │                    │                 │ validate_format  │                   │
   │                   │                    │                 │─────────┐        │                   │
   │                   │                    │                 │         │        │                   │
   │                   │                    │                 │◀────────┘        │                   â            │                    │                 │                  │                   │
   │                   │                    │                 │ extract_contact  │                   │
   │                   │                    │                 │─────────────────▶│                   │
   │                   │                    │                 │                  │                   │
   │                   │              │                 │                  │ Gemini API call   │
   │                   │                    │                 │                  │──────────┐        │
   │                   │                    │                 │                  │          │        │
   │                   │                    │                 │                  │◀─────────┘        │
   │                   │                        │                  │                   │
   │                   │                    │                 │    JSON result   │                   │
   │                   │                    │                 │◀─────────────────│                   │
   │                   │                    │                 │                  │                   │
   │                   │                    │ {success, contact}             │                   │
   │                   │                    │◀────────────────│                  │                   │
   │                   │                    │                 │                  │                   │
   │                   │                    │ save_contact    │                  │                   │
   │                   │                    │───────────────────────────────────────▶  │
   │                   │                    │                 │                  │                   │
   │                   │                    │                 │                  │    POST /contacts │
   │                   │                    │                 │                  │    ───────────┐   │
   │                   │                    │           │                  │               │   │
   │                   │                    │                 │                  │    ◀──────────┘   │
   │                   │                    │                 │                  │                   │
   │                   │                    │ {success, contact_id}              │                   │
   │                   │                    │◀───────────────────────────────────────────────  │
   │                   │                    │                 │                  │                   │
   │                   │  sendMessage       │                 │                  │                   │
   │                   │◀───────────────────│                 │                  │                   │
   │                 │                    │                 │                  │                   │
   │  ✅ Confirmación  │                    │                 │                  │                   │
   │◀──────────────────│                    │                 │                  │                   │
   │                   │                    │                 │                  │                   │
```

### 12.2 Flujo Alternativo: Usu Autorizado

```
┌──────┐          ┌──────────┐       ┌─────────────┐      ┌─────────┐
│ User │          │ Telegram │       │ Orchestrator│      │ Security│
└──┬───┘          └────┬─────┘       └──────┬──────┘      └────┬────┘
   │                   │                    │                  │
   │  EnvÃensaje    │                    │                  │
   │──────────────────▶│                    │                  │
   │                   │                    │                  │
   │                   │  Update (message)  │                  │
   │                   │───────────────────▶│                  │
   │                   │                    │                  │
   │     │                    │ process_request  │
   │                   │                    │─────────────────▶│
   │                   │                    │                  │
   │                   │                    │                  │ validate_origin
   │                   │                    │                  │────────┐
   │                   │                    │                  │        │ user_id  │                   │                    │                  │◀───────┘ in whitelist
   │                   │                    │                  │
   │                   │                    │ {success: false, │
   │                   │                    │  error: "No autorizado"}
   │                   │                    │◀─────────────────│
   │                   │                    │                     │                   │  sendMessage       │                  │
   │                   │◀───────────────────│                  │
   │                   │                    │                  │
   │  ❌ No autorizado │                    │                  │
   │◀──────────────────│                    │                  │
   │                   │                    │                 .3 Flujo Alternativo: Error en Gemini

```
┌──────┐          ┌──────────┐       ┌─────────────┐      ┌─────────┐      ┌────────┐
│ User │          │ Telegram │       │ Orchestrator│      │ Security│      │ Gemini │
└──┬───┘          └────┬─────┘       └──────┬──────┘      └────┬────┘      └───┬────┘
   │                   │                    │                  │               │
   │  Envía mensaje    │                    │                  │               │
   │──────────────────▶│                    │                  │               │
   │                   │                    │                  │               │
   │                   │  Update            │                  │    │
   │                   │───────────────────▶│                  │               │
   │                   │                    │                  │               │
   │                   │                    │ process_request  │               │
   │                   │                    │─────────────────▶│               │
   │                   │                    │                      │
   │                   │                    │                  │ validate ✓    │
   │                   │                    │                  │───────┐       │
   │                   │                    │                  │◀──────┘       │
   │                   │                    │                  │               │
   │                   │                    │                  │ extract_contact
   │             │                    │                  │──────────────▶│
   │                   │                    │                  │               │
   │                   │                    │                  │               │ API Error
   │                   │                    │                  │               │────┐
   │                   │                    │                  │               │◀───┘
   │               │                    │                  │               │
   │                   │                    │                  │ {success: false,
   │                   │                    │                  │  error: "Gemini API error"}
   │                   │                    │                  │◀──────────────│
   │                   │                    │                  │               │
   │                   │      │ {success: false} │               │
   │                   │                    │◀─────────────────│               │
   │                   │                    │                  │               │
   │                   │  sendMessage       │                  │               │
   │                   │◀───────────────────│                  │               │
   │                   â      │                  │               │
   │  ❌ Error proceso │                    │                  │               │
   │◀──────────────────│                    │                  │               │
   │                   │                    │                  │               │
```

---

## 13. Seguridad

### 13.1 Modelo de Amenazas

| ID | Amenaza | Probabilidad | Impacto | Mitigación |
|----|---------|--------------|---------|
| T-01 | Acceso no autorizado | Media | Alto | Whitelist de usuarios |
| T-02 | Inyección de código | Baja | Alto | Sanitización de inputs |
| T-03 | DDoS / Flood | Media | Medio | Rate limiting |
| T-04 | Exposición de API keys | Baja | Crítico | Variables de entorno |
| T-05 | Man-in-the-middle | Baja | Alto | TLS obligatorio |
| T-06 | Data leakage en logs | Media | Medio | Ofuscación de datos sensibles |

### 13.2 Controles de Seguridad

#### 13.2.1 Autenticación y Autorización

```python
entación de whitelist
class AuthorizationService:
    def __init__(self, allowed_users: List[int]):
        self.allowed_users = set(allowed_users)
        self.blocked_users = set()
        self.failed_attempts = defaultdict(int)
    
    def is_authorized(self, user_id: int) -> bool:
        # Verificar si está bloqueado
        if user_id in self.blocked_users:
            return False
        
        # Verificar si está autorizado
        if user_id in self.allowed_users:
            return True
     
        # Registrar intento fallido
        self.failed_attempts[user_id] += 1
        
        # Bloquear después de 5 intentos
        if self.failed_attempts[user_id] >= 5:
            self.blocked_users.add(user_id)
            logger.warning(f"User {user_id} blocked after 5 failed attempts")
        
        return False
```

#### 13.2.2 Rate Limiting

```python
from collections import defaultdict
from time import time

class RateLimiter:
    def __init__(self, max_requests: int = 10, window_second: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
    
    def is_allowed(self, user_id: int) -> bool:
        now = time()
        window_start = now - self.window_seconds
        
        # Limpiar requests antiguos
        self.requests[user_id] = [
            t for t in self.requests[user_id] if t > window_start
        ]
        
        # Verificar límite
        if len(self.requests[user_id]) >= self.max_requsts:
            return False
        
        # Registrar nuevo request
        self.requests[user_id].append(now)
        return True
```

#### 13.2.3 Sanitización de Datos

```python
import re
import html

class DataSanitizer:
    # Patrones peligrosos
    DANGEROUS_PATTERNS = [
        r'<script.*?>.*?</script>',  # Scripts
        r'javascript:',               # JavaScript protocol
        r'on\w+\s*=',                # Event handlers
        r'\$\{.*?\}',                # Template injection
        r\{\{.*?\}\}',              # Jinja/Mustache
    ]
    
    @classmethod
    def sanitize(cls, text: str) -> str:
        if not text:
            return ""
        
        # HTML escape
        sanitized = html.escape(text)
        
        # Remover patrones peligrosos
        for pattern in cls.DANGEROUS_PATTERNS:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        # Limitar longitud
        sanitized = sanitized[:1000]
        
        return sanitized.strip()
```

### 13.3 Gestión de Secretos

```yaml
# Política de gestión de secretos

Almacenamiento:
  - Variables de entorno para desarrollo
  - HashiCorp Vault o AWS Secrets Manager para producción
  - Nunca en código fuente o logs

Rotación:
  - API keys: Cada 90 días
  - Bot token: Cada 180 días o si se compromete

Acceso:
  - Principio de mínimo privilegio
  - Logging de acceso a secretos
  - Separación por ambiente (dev/staging/prod)
```

### 13.4 Logging de Seguridad

```python
import logging
from dport datetime

class SecurityLogger:
    def __init__(self):
        self.logger = logging.getLogger('security')
        self.logger.setLevel(logging.INFO)
    
    def log_access_attempt(self, user_id: int, authorized: bool, ip: str = None):
        self.logger.info({
            "event": "access_attempt",
            "user_id": user_id,
            "authorized": authorized,
            "ip": ip,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def log_rate_limit_exceeded(self, user_id: int):
        self.logger.warning({
            "event": "rate_limit_exceeded",
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def log_suspicious_input(self, user_id: int, input_type: str):
        self.logger.warning({
            "event": "suspicious_input",
            "user_id": user_id,
            "input_type": input_type,
            "timestamp": datetime.utcnow().isoformat()
        })
```

---

## 14. Plan de Pruebas

### 14.1 Estrategia de Pruebas

```
┌─────────────────────────────────────────────────────────────────┐
│                    PIRÁMIDE DE PRUEBAS                          │
├─────────────────────────────────────────────────────────────────┤
│                                                              │
│                          ┌─────┐                                │
│                         /  E2E  \                               │
│                        /─────────\        10%                   │
│                       / Integration\                            │
│                      /───────────────\    20%                   │
│                     /    Unit   \                         │
│                    /───────────────────\  70%                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 14.2 Casos de Prueba Unitarias

#### 14.2.1 SecurityAgent Tests

```python
# tests/testity_agent.py

import pytest
from unittest.mock import AsyncMock, patch
from src.agents.security_agent import SecurityAgent

class TestSecurityAgent:
    
    @pytest.fixture
    def agent(self):
        return SecurityAgent(
            gemini_api_key="test_key",
            allowed_users=[123456789]
        )
    
    @pytest.mark.asyncio
    async def test_authorized_user_passes_validation(self, agent):
        """TC-SEC-001: Usuario autorizado pasa validación"""
        message = {
            "text": "uan Pérez 3001234567 recomendado por María",
            "user_id": 123456789,
            "chat_id": 1
        }
        
        with patch.object(agent.gemini_service, 'extract_contact_info') as mock:
            mock.return_value = {
                "success": True,
                "data": {
                    "nombre": "Juan Pérez",
                    "telefono": "+573001234567",
                    "quien_lo_recomendo": "María"
                }
            }
            
            result = awagent.process_request(message)
            
            assert result["success"] is True
            assert "contact" in result
    
    @pytest.mark.asyncio
    async def test_unauthorized_user_rejected(self, agent):
        """TC-SEC-002: Usuario no autorizado es rechazado"""
        message = {
            "text": "Cualquier mensaje",
            "user_id": 999999999,  # No autorizado
            "chat_id": 1
        }
        
        result = await agent.process_request(message)
        
        assert result["success"] is False
        assert "no autorizado" in result["error"].lower()
    
    @pytest.mark.asyncio
    async def test_short_message_rejected(self, agent):
        """TC-SEC-003: Mensaje muy corto es rechazado"""
        message = {
            "text": "Hola",
            "user_id": 123456789,
            "chat_id": 1
        }
        
        result = await agent.process_request(message)
        
        assert result["success"] is False
    
    @pytest.mark.asyncio
    async def test_missing_fields_detected(self, agent):
        """TC-SEC-004: Campos faltantes son detectados"""
        message = {
            "text": "Juan sin teléfono",
            "user_id": 123456789,
            "chat_id": 1
        }
        
        with patch.object(agent.gemini_service, 'extract_contact_info') as mock:
            mock.return_value = {
                "success": True,
                "data": {
                    "nombre": "Juan",
                    "telefono": "",
                    "quien_lo_rcomendo": ""
                }
            }
            
            result = await agent.process_request(message)
            
            assert result["success"] is False
            assert "faltantes" in result["error"].lower()
```

#### 14.2.2 GeminiService Tests

```python
# tests/test_gemini_service.py

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.services.gemini_service import GeminiService

class TestGeminiService:
    
    @pytest.fixture
    def service(self):
        with patch('google.generativeai.configure'):
            with patch('google.generativeai.GenerativeModel'):
                return GeminiService(api_key="test_key")
    
    @pytest.mark.asyncio
    async def test_extract_complete_contact(self, service):
        """TC-GEM-001: Extracción completa de contacto"""
        mock_response = MagicMock()
        mock_response.text = '''
        {
            "nombre": "Juan Carlos Pérez",
            "telefono": "3001234567",
            "quien_lo_recomendo""María López"
        }
        '''
        
        service.model.generate_content_async = AsyncMock(return_value=mock_response)
        
        result = await service.extract_contact_info(
            "Juan Carlos Pérez, celular 300 123 4567, me lo recomendó María López"
        )
        
        assert result["success"] is True
        assert result["data"]["nombre"] == "Juan Carlos Pérez"
        assert "3001234567" in result["data"]["telefono"]
        assert result["data"]["quien_lo_recomendoMaría López"
    
    @pytest.mark.asyncio
    async def test_phone_normalization(self, service):
        """TC-GEM-002: Normalización de teléfono"""
        phone = service._normalize_phone("300 123 4567")
        assert phone == "+573001234567"
        
        phone = service._normalize_phone("+57 315-789-4561")
        assert phone == "+573157894561"
    
    @pytest.mark.asyncio
    async def test_handles_invalid_json(self, service):
        """TC-GEM-003: Manejo de JSON inválido"""
        mock_rse = MagicMock()
        mock_response.text = "Esto no es JSON válido"
        
        service.model.generate_content_async = AsyncMock(return_value=mock_response)
        
        result = await service.extract_contact_info("cualquier texto")
        
        assert result["success"] is False
        assert "error" in result
```

#### 14.2.3 Contact Model Tests

```python
# tests/test_models.py

import pytest
from pydantic import ValidationError
from src.models.contact import Contact

class TestContactMoel:
    
    def test_valid_contact_creation(self):
        """TC-MOD-001: Creación de contacto válido"""
        contact = Contact(
            nombre="Juan Pérez",
            telefono="3001234567",
            quien_lo_recomendo="María"
        )
        
        assert contact.nombre == "Juan Pérez"
        assert contact.telefono == "+573001234567"
        assert contact.source == "telegram"
    
    def test_phone_normalization(self):
        """TC-MOD-002: Normalización automática de teléfono    contact = Contact(
            nombre="Test",
            telefono="300 123 4567",
            quien_lo_recomendo="Test"
        )
        
        assert contact.telefono == "+573001234567"
    
    def test_empty_name_rejected(self):
        """TC-MOD-003: Nombre vacío es rechazado"""
        with pytest.raises(ValidationError):
            Contact(
                nombre="",
                telefono="3001234567",
                quien_lo_recomendo="María"
            )
    
    def test_invalid_pho_rejected(self):
        """TC-MOD-004: Teléfono inválido es rechazado"""
        with pytest.raises(ValidationError):
            Contact(
                nombre="Juan",
                telefono="123",  # Muy corto
                quien_lo_recomendo="María"
            )
```

### 14.3 Casos de Prueba de Integración

```python
# tests/test_integration.py

import pytest
from unittest.mock import patch, AsyncMock
from src.main import ContactsOrchestrator

class TestIntegration:
    
    @pytest.fixture
  f orchestrator(self):
        config = {
            "gemini_api_key": "test_key",
            "contacts_api_url": "https://api.test.com",
            "contacts_api_key": "test_key",
            "allowed_users": [123456789]
        }
        return ContactsOrchestrator(config)
    
    @pytest.mark.asyncio
    async def test_full_flow_success(self, orchestrator):
        """TC-INT-001: Flujo completo exitoso"""
        # Mock Gemini
        with patch.object(
            orchestrator.security_agent.gemini_service,
            'extract_contact_info'
        ) as mock_gemini:
            mock_gemini.return_value = {
                "success": True,
                "data": {
                    "nombre": "Juan Pérez",
                    "telefono": "+573001234567",
                    "quien_lo_recomendo": "María"
                }
            }
            
            # Mock API Contactos
            with patch.object(
                orchestrator.persistence_agent,
                'save_contact'
          ) as mock_save:
                mock_save.return_value = {
                    "success": True,
                    "contact_id": "uuid-123"
                }
                
                # Simular mensaje de Telegram
                message = {
                    "text": "Juan Pérez 3001234567 recomendado por María",
                    "user_id": 123456789,
                    "chat_id": 1
                }
                
                # Procesar
                result = await orchestrator.secuty_agent.process_request(message)
                assert result["success"] is True
                
                save_result = await orchestrator.persistence_agent.save_contact(
                    result["contact"]
                )
                assert save_result["success"] is True
```

### 14.4 Matriz de Cobertura de Pruebas

| Componente | Unit Tests | Integration | E2E | Cobertura |
|------------|------------|-------------|-----|-----------|
| SecurityAgent | 15 | 3 | 1 | 95% |
| PersistenceAgent | 8 | 2 | 1 | 90% |
| GeminiService | 10 | 2 | 1 | 88% |
| Contact Model | 12 | - | - | 100% |
| Validators | 8 | - | - | 92% |
| **Total** | **53** | **7** | **3** | **93%** |

---

## 15. Riesgos y Mitigaciones

### 15.1 Matriz de Riesgos

| ID | Riesgo | Probabilidad | Impacto | Severidad | Mitigación |
|----|--------|--------------|---------|-----------|------------|
| R-01 | Caída de Gemini API | Media | Alto | Alta | Fallback con regex, cache de prompts |
| R-02 | Límite de rate de Telegram | BajaMedio | Media | Queue de mensajes, rate limiting interno |
| R-03 | Datos incorrectos de Gemini | Media | Medio | Media | Validación estricta, confirmación usuario |
| R-04 | Caída de API de contactos | Baja | Alto | Media | Retry con backoff, queue de persistencia |
| R-05 | Costos excesivos de Gemini | Media | Medio | Media | Monitoreo, límites diarios, caching |
| R-06 | Usuarios malintencionados | Baja | Alto | Media | Rate limiting, logging, bloqueo automático |

### 15.2 Plan de Contingencia

###1: Caída de Gemini API

```python
class GeminiServiceWithFallback:
    async def extract_contact_info(self, text: str) -> dict:
        try:
            # Intentar con Gemini
            result = await self._extract_with_gemini(text)
            return result
        except Exception as e:
            logger.warning(f"Gemini failed: {e}, using fallback")
            # Fallback con regex
            return self._extract_with_regex(text)
    
    def _extract_with_regex(self, text: str) -> dict:
        """Etracción básica con expresiones regulares"""
        import re
        
        phone_pattern = r'[\+]?[\d\s\-]{10,15}'
        phone_match = re.search(phone_pattern, text)
        
        rec_pattern = r'(?:recomendado|referido|de parte de)\s+(\w+)'
        rec_match = re.search(rec_pattern, text, re.IGNORECASE)
        
        # Asumir que el nombre es el texto antes del teléfono
        name = text[:phone_match.start()].strip() if phone_match else ""
        
        return {
            "success": e,
            "data": {
                "nombre": name,
                "telefono": phone_match.group() if phone_match else "",
                "quien_lo_recomendo": rec_match.group(1) if rec_match else ""
            },
            "fallback": True
        }
```

### 15.3 Monitoreo de Riesgos

| Riesgo | Métrica | Umbral Alerta | Acción |
|--------|---------|---------------|--------|
| R-01 | Error rate Gemini | > 5% | Activar fallback |
| R-02 | Mensajes en cola | > 100 | Escalar instancias |
| R-03 | sa de corrección | > 10% | Ajustar prompts |
| R-04 | Latencia API contactos | > 5s | Activar retry |
| R-05 | Costo diario Gemini | > $X | Notificar admin |

---

## 16. Cronograma

### 16.1 Fases del Proyecto

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CRONOGRAMA DEL PROYECTO                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Semana    1    2    3    4    5    6    7    8                            │
│            │    │    │    │    │    │    │    │                  │
│  FASE 1    ████████████                                                    │
│  Diseño    │    │    │                                                     │
│            │    │    │                                                     │
│  FASE 2         │    ████████████████████                                  │
│  Desarrollo     │    │    │    │    │                                      │
   │    │    │    │    │                                      │
│  FASE 3              │    │    │    ████████████                           │
│  Pruebas              │    │    │    │    │                                │
│                       │    │    │    │    │                                │
│  FASE 4                    │    │    │    ████████                         │
│  Deploy                         │    │    │                          │
│                             │    │    │    │    │                          │
│  FASE 5                          │    │    │    ████                       │
│  Soporte                          │    │    │    │                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────┘
```

### 16.2 Detalle de Actividades

| Fase | Actividad | Duración | Responsable | Entregable |
|------|-----------|----------|-------------|------------|
| **1. Diseño** | Definición de arquitectura | 3 días | Tech Lead | Diagrama de arquitectura |
| | Diseño de modelo de datos | 2 días | Backend Dev | Esquemas JSON |
| | Diseño de interfaces | 2 días | Backend Dev | EspecificacióIs |
| | Revisión y aprobación | 2 días | Product Owner | PRD/SRS aprobado |
| **2. Desarrollo** | Setup del proyecto | 2 días | Backend Dev | Repo configurado |
| | Implementación SecurityAgent | 5 días | Backend Dev | Agente funcional |
| | Integración Gemini | 3 días | Backend Dev | Servicio de extracción |
| | Implementación PersistenceAgent | 3 días | Backend Dev | Agente de persistencia |
| | Integración Telegram | 3 días | Backend Dev | Bot funcional |
| **3. Pruebas** | Unit tests | 4 dite de pruebas |
| | Integration tests | 3 días | QA | Pruebas de integración |
| | UAT | 3 días | Product Owner | Sign-off |
| **4. Deploy** | Configuración infraestructura | 2 días | DevOps | Servidor configurado |
| | Despliegue a producción | 1 día | DevOps | Sistema en producción |
| | Monitoreo | 2 días | DevOps | Dashboards activos |
| **5. Soporte** | Documentación | 2 días | Tech Lead | Docs completos |
| | Capacitación | 1 día | Tech Lead | Usuarios capacitados |

### 16.3 Hitos del Pto | Fecha Objetivo | Criterio de Éxito |
|------|----------------|-------------------|
| M1: Diseño completado | Semana 2 | PRD/SRS aprobado |
| M2: MVP funcional | Semana 5 | Bot procesa mensajes correctamente |
| M3: Pruebas completadas | Semana 6 | Cobertura > 80%, 0 bugs críticos |
| M4: Go-live | Semana 7 | Sistema en producción |
| M5: Cierre | Semana 8 | Documentación y capacitación completa |

---

## 17. Métricas de Éxito

### 17.1 KPIs del Producto

| Métrica | Objetivo | Medición |
|----------|----------|
| Tiempo de registro | < 5 segundos | P95 de latencia end-to-end |
| Precisión de extracción | > 95% | Contactos correctos / Total |
| Disponibilidad | 99.5% | Uptime mensual |
| Adopción | 80% usuarios activos | Usuarios activos / Autorizados |
| Satisfacción | > 4.0 / 5.0 | Encuesta de usuarios |

### 17.2 KPIs Técnicos

| Métrica | Objetivo | Herramienta |
|---------|----------|-------------|
| Cobertura de código | > 80% | pytest-cov |
| Tiempo de respuesta Gemini | < 3s | Prs |
| Error rate | < 1% | Grafana |
| Memory usage | < 512MB | Docker stats |
| CPU usage | < 50% promedio | CloudWatch |

### 17.3 Dashboard de Monitoreo

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DASHBOARD DE MONITOREO                              │
├───────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐ │
│  │   MENSAJORA     │  │   TASA DE ÉXITO     │  │   LATENCIA P95      │ │
│  │                     │  │                     │  │                     │ │
│  │       ▲ 127         │  │       98.5%         │  │       2.3s          │ │
│  │    ───┴───          │  │    ████████░░       │  │    ▔▔▔▁▁▁▁         │ │
│  └─────────────────────┘  └────────────────────┘  └─────────────────────┘ │
│                                                                             │
│  ┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐ │
│  │   ERRORES (24h)     │  │   UPTIME            │  │   COSTO GEMINI      │ â              │  │                     │  │                     │ │
│  │         3           │  │       99.7%         │  │      $12.50         │ │
│  │    ▁▁▁▂▁▁▁▁         │  │    ████████████░    │  │    ──────────       │ │
│  └─────────────────────┘  └─────────────────────┘  └─────────â
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 18. Glosario

| Término | Definición |
|---------|------------|
| **Agente** | Componente autónomo del sistema que realiza una función específica |
| **API** | Interfaramación de Aplicaciones |
| **Bot** | Programa automatizado que interactúa con usuarios vía Telegram |
| **Gemini** | Modelo de lenguaje grande de Google para procesamiento de texto |
| **JSON** | Formato de intercambio de datos basado en texto |
| **LLM** | Large Language Model - Modelo de lenguaje grande |
| **NLP** | Natural Language Processing - Procesamiento de lenguaje natural |
| **Polling** | Técnica de obtención de actualizaciones consultando periódicamente |
| **Rate Limiting** | Control deencia de peticiones |
| **REST** | Estilo arquitectónico para servicios web |
| **Sanitización** | Proceso de limpiar datos de entrada para seguridad |
| **Webhook** | Callback HTTP para notificaciones en tiempo real |
| **Whitelist** | Lista de elementos permitidos |

---

## 19. Apéndices

### Apéndice A: Dependencias del Proyecto

```
# requirements.txt

# Core
python-telegram-bot==21.0
google-generativeai==0.5.0
httpx==0.27.0
pydantic==2.6.0
pydantic-settings==2.2.0

# Utilities
python-dotenv==1.0.0acity==8.2.0

# Logging
structlog==24.1.0

# Testing
pytest==8.0.0
pytest-asyncio==0.23.0
pytest-cov==4.1.0

# Development
black==24.1.0
flake8==7.0.0
mypy==1.8.0
```

### Apéndice B: Prompt de Gemini

```python
EXTRACTION_PROMPT = """
Eres un asistente especializado en extraer información de contactos de mensajes de texto en español.

Tu tarea es analizar el mensaje proporcionado y extraer la siguiente información:
1. Nombre completo del contacto
2. Número de teléfono
3. Nombre de la persona que reco/refiere el contacto

REGLAS:
- El nombre puede estar en cualquier parte del mensaje
- El teléfono puede tener diferentes formatos (con espacios, guiones, paréntesis)
- El referido puede mencionarse con frases como "recomendado por", "de parte de", "me lo pasó", etc.
- Si no encuentras algún dato, devuelve cadena vacía ""

IMPORTANTE: Responde ÚNICAMENTE con un JSON válido, sin explicaciones adicionales.

Formato de respuesta:
{
    "nombre": "nombre completo extraído",
    "telefono": "número de tsolo dígitos y + si aplica)",
    "quien_lo_recomendo": "nombre del referido"
}

Mensaje a procesar:
{message}
"""
```

### Apéndice C: Configuración de Docker

```dockerfile
# Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/
COPY config/ ./config/
COPY main.py .

# Environment
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Run
CMD ["python", "main.py"]
```

```y
# docker-compose.yml

version: '3.8'

services:
  bot:
    build: .
    container_name: contacts-agent
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - ./logs:/app/logs
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    healthcheck:
      test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:8080/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
```

### Apéndice D: Checklist de Despligue

```markdown
## Pre-Despliegue

- [ ] Variables de entorno configuradas
- [ ] API keys válidas y activas
- [ ] Bot de Telegram creado y token obtenido
- [ ] Usuarios autorizados definidos
- [ ] Tests pasando (cobertura > 80%)
- [ ] Código revisado y aprobado

## Despliegue

- [ ] Imagen Docker construida
- [ ] Contenedor desplegado
- [ ] Health check pasando
- [ ] Logs funcionando
- [ ] Monitoreo activo

## Post-Despliegue

- [ ] Prueba de mensaje de Telegram
- [ ] Verificar contacto guardado en API
- ] Verificar notificación al usuario
- [ ] Dashboards de monitoreo revisados
- [ ] Documentación actualizada
- [ ] Usuarios notificados
```

---

## Historial de Revisiones

| Versión | Fecha | Autor | Cambios |
|---------|-------|-------|---------|
| 1.0 | Diciembre 2025 | Equipo de Desarrollo | Versión inicial |

---

**Fin del Documento**

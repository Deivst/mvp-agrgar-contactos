-- ================================================
-- Script de inicialización de base de datos
-- Sistema Multi-Agente de Gestión de Contactos
-- ================================================

-- Crear base de datos si no existe
-- (ejecutar como superusuario)
-- CREATE DATABASE contacts_db;

-- Conectar a la base de datos
\c contacts_db;

-- Crear extensión para UUIDs si no existe
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ================================================
-- Tabla: contacts
-- ================================================

CREATE TABLE IF NOT EXISTS contacts (
    id VARCHAR(36) PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    quien_lo_recomendo VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    source VARCHAR(50) DEFAULT 'telegram',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ================================================
-- Índices para optimizar consultas
-- ================================================

CREATE INDEX IF NOT EXISTS idx_contacts_nombre ON contacts(nombre);
CREATE INDEX IF NOT EXISTS idx_contacts_telefono ON contacts(telefono);
CREATE INDEX IF NOT EXISTS idx_contacts_created_at ON contacts(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_contacts_source ON contacts(source);

-- ================================================
-- Trigger para actualizar updated_at automáticamente
-- ================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_contacts_updated_at
    BEFORE UPDATE ON contacts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ================================================
-- Grants (ajustar según el usuario de la aplicación)
-- ================================================

-- GRANT ALL PRIVILEGES ON TABLE contacts TO your_app_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO your_app_user;

-- ================================================
-- Datos de ejemplo (opcional - comentar en producción)
-- ================================================

-- INSERT INTO contacts (id, nombre, telefono, quien_lo_recomendo, timestamp, source)
-- VALUES
--     (uuid_generate_v4(), 'Juan Pérez García', '+573001234567', 'María López', NOW(), 'telegram'),
--     (uuid_generate_v4(), 'Ana María Rodríguez', '+573157894561', 'Carlos Ruiz', NOW(), 'telegram');

-- ================================================
-- Verificar la creación
-- ================================================

SELECT
    'contacts' as table_name,
    COUNT(*) as row_count
FROM contacts;

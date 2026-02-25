-- Estructura inicial para el esquema de Vacantes

CREATE TABLE IF NOT EXISTS estado (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL -- Se agregó UNIQUE para que funcione el ON CONFLICT
);

INSERT INTO estado (nombre) VALUES ('Activo'), ('Inactivo'), ('Pendiente')
ON CONFLICT (nombre) DO NOTHING;

-- CREATE TABLE IF NOT EXISTS rol (
--     id SERIAL PRIMARY KEY,
--     nombre VARCHAR(50) NOT NULL,
--     fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     fecha_actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

CREATE TABLE IF NOT EXISTS usuario (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) UNIQUE NOT NULL,
    password TEXT NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- CREATE TABLE IF NOT EXISTS tipo_contrato (
--     id SERIAL PRIMARY KEY,
--     nombre VARCHAR(100) NOT NULL,
--     fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     fecha_actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     usuario_creacion INT REFERENCES usuario(id),
--     usuario_actualizacion INT REFERENCES usuario(id)
-- );

-- CREATE TABLE IF NOT EXISTS tipo_modalidad (
--     id SERIAL PRIMARY KEY,
--     nombre VARCHAR(100) NOT NULL,
--     fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     fecha_actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     usuario_creacion INT REFERENCES usuario(id),
--     usuario_actualizacion INT REFERENCES usuario(id)
-- );

CREATE TABLE IF NOT EXISTS empresas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(150) UNIQUE NOT NULL, -- Se agregó UNIQUE para evitar errores en el insert
    nombre_log VARCHAR(150) NOT NULL, -- Se agregó UNIQUE para evitar errores en el insert
    subdominio VARCHAR(100),
    proveedor VARCHAR(100),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion INT REFERENCES usuario(id),
    usuario_actualizacion INT REFERENCES usuario(id),
    id_estado INT REFERENCES estado(id)
);

-- Inserts solicitados (ahora en minúsculas para coincidir con la tabla)
INSERT INTO empresas (nombre, nombre_log, subdominio, proveedor, id_estado) 
VALUES ('Grupo Palmon', 'PALMON','grupopalmon', 'hiringroom', 1)
ON CONFLICT (nombre) DO NOTHING;

INSERT INTO empresas (nombre, nombre_log, subdominio, proveedor, id_estado) 
VALUES ('ECUAQUIMICA', 'ECUAQUIMICA','ecuaquimica', 'hiringroom', 1)
ON CONFLICT (nombre) DO NOTHING;

CREATE TABLE IF NOT EXISTS vacantes (
    id SERIAL PRIMARY KEY,
    id_empresa INT REFERENCES empresas(id),
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    identificador VARCHAR(100) UNIQUE, -- UUID extraído de la URL
    url TEXT,
    -- Nuevos campos agregados
    ubicacion VARCHAR(150),
    area VARCHAR(150),
    modalidad VARCHAR(100),
    tipo_contrato VARCHAR(100),
    -------------------------
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion INT REFERENCES usuario(id),
    usuario_actualizacion INT REFERENCES usuario(id),
    id_estado INT REFERENCES estado(id)
);
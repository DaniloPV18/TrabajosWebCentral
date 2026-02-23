
-- Estructura inicial para el esquema de Vacantes

CREATE TABLE IF NOT EXISTS Estado (
    id SERIAL PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS Rol (
    id SERIAL PRIMARY KEY,
    Nombre VARCHAR(50) NOT NULL,
    FechaRegistro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FechaActualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS Usuario (
    id SERIAL PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Correo VARCHAR(100) UNIQUE NOT NULL,
    Password TEXT NOT NULL,
    FechaRegistro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FechaActualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS TipoContrato (
    id SERIAL PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    FechaRegistro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FechaActualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UsuarioCreacion INT REFERENCES Usuario(id),
    UsuarioActualizacion INT REFERENCES Usuario(id)
);

CREATE TABLE IF NOT EXISTS TipoModalidad (
    id SERIAL PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    FechaRegistro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FechaActualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UsuarioCreacion INT REFERENCES Usuario(id),
    UsuarioActualizacion INT REFERENCES Usuario(id)
);

CREATE TABLE IF NOT EXISTS Empresas (
    id SERIAL PRIMARY KEY,
    Nombre VARCHAR(150) NOT NULL,
    Subdominio VARCHAR(100),
    Proveedor VARCHAR(100),
    FechaRegistro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FechaActualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UsuarioCreacion INT REFERENCES Usuario(id),
    UsuarioActualizacion INT REFERENCES Usuario(id),
    IDEstado INT REFERENCES Estado(id)
);

CREATE TABLE IF NOT EXISTS Vacantes (
    id SERIAL PRIMARY KEY,
    IDEmpresa INT REFERENCES Empresas(id),
    Titulo VARCHAR(255) NOT NULL,
    Descripcion TEXT,
    Identificador VARCHAR(100) UNIQUE, -- CRÍTICO: Para evitar duplicados en scraping
    Url TEXT,
    FechaRegistro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FechaActualizado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UsuarioCreacion INT REFERENCES Usuario(id),
    UsuarioActualizacion INT REFERENCES Usuario(id),
    IDTipoContrato INT REFERENCES TipoContrato(id),
    IDTipoModalidad INT REFERENCES TipoModalidad(id),
    IDEstado INT REFERENCES Estado(id)
);
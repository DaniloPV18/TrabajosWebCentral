# 🕷️ TrabajosWeb Central - Plataforma de Web Scraping

Plataforma automatizada multi-servicio para la extracción de vacantes de portales de empleo y centralización en PostgreSQL. Utiliza Docker Compose para orquestación y comunicación entre servicios.

---

## 📋 Servicios Disponibles

### 1️⃣ **Web Scraper** (Python)
Automatiza la extracción de vacantes de portales de empleo (HiringRoom) y las centraliza en PostgreSQL. Está diseñado para ejecutarse de forma aislada mediante contenedores.

#### 🚀 Comandos Principales
| Acción | Comando |
|--------|---------|
| Construir e Iniciar | `docker-compose up -d --build` |
| Ver Logs (Progreso) | `docker logs -f trabajos_scraper` |
| Ejecución Manual | `docker exec -it trabajos_scraper python /app/src/main.py` |
| Detener Servicio | `docker-compose stop scraper` |

#### 🛠️ Configuración del Entorno
El scraper utiliza las siguientes variables definidas en `docker-compose.yml`:
- **DB Host**: `database` (nombre del servicio en la red Docker)
- **Logs Service**: `http://logs_service:8000` (comunicación HTTP one-way)
- **Logs Path**: `/app/logs` (mapeado a `./logs_storage/scraping` para persistencia local)
- **Python Path**: `/app/src` (raíz del proyecto)

#### 📦 Componentes Internos
- **domain/models.py**: Dataclass `Vacante` con campos obligatorios y opcionales
- **application/scraper_service.py**: Orquestador que gestiona empresas y motores
- **infrastructure/adapters/**: Repositorio PostgreSQL, Logger HTTP, HiringRoom Engine
- **infrastructure/config.py**: Cargador de configuración basado en `.env`

---

### 2️⃣ **Logs Service** (FastAPI)
Servicio centralizado de logging que recibe eventos HTTP del scraper y persiste registros en el almacenamiento.

#### 🔗 API Endpoints
- **POST `/escribir-log`**: Recibe logs asincronos del scraper
  ```json
  {
    "nombre_log": "WEB_PALMON",
    "mensaje": "[OUT] Extraído: Ingeniero de Sistemas",
    "tipo": "INFO|WARNING|ERROR"
  }
  ```
- **GET `/health`**: Verifica disponibilidad del servicio
  ```json
  {
    "status": "online",
    "service": "logs-central"
  }
  ```

#### 📁 Ubicación de Logs
```
logs_storage/
├── scraping/       (Registros del scraper)
├── database/       (Registros de base de datos)
└── others/         (Otros registros)
```

---

### 3️⃣ **Frontend** (Next.js 16)
Interfaz de usuario React-based para visualizar y gestionar vacantes. Estado actual: configuración mínima.

#### 📝 Scripts Disponibles
```bash
npm run dev    # Iniciar servidor de desarrollo (puerto 3000)
npm run build  # Compilar para producción
npm start      # Ejecutar build final
npm run lint   # Ejecutar ESLint
```

#### 🎨 Stack Tecnológico
- Next.js 16.1.6
- React 19.2.3
- TypeScript 5
- Tailwind CSS 4
- ESLint 9

---

### 4️⃣ **Database** (PostgreSQL 16)
Almacenamiento centralizado para todas las vacantes y metadatos. Inicialización automática con `init.sql`.

#### 📊 Tablas Principales
- **empresas**: Configuración de portales a scrapear (nombre, subdomain, proveedor)
- **vacantes**: Registros de empleos (título, URL, ubicación, modalidad, etc.)
- **usuario**: Usuarios del sistema
- **estado**: Estados para control de activos/inactivos

#### 🔑 Conexión
```
Host: database
Puerto: 5432
Usuario: ${DB_USER} (en .env)
Base de datos: ${DB_NAME} (en .env)
```

---

## ⚙️ Comunicación Entre Servicios

```
┌─────────────┐           ┌──────────────┐
│   Scraper   │──HTTP────▶│ Logs Service │
│  (Python)   │ /escribir  │  (FastAPI)   │
└──────┬──────┘           └──────────────┘
       │
       │ psycopg2
       ▼
┌─────────────────────┐
│   PostgreSQL 16     │
│   (Database)        │
│  docker network: ▶  │◀ todos los servicios
└─────────────────────┘
```

---

## 🔧 Mantenimiento y Reseteo de Datos

### ⚠️ Mantenimiento Básico
Si realizas cambios estructurales en `init.sql` (agregar columnas, nuevas tablas), Docker no los aplicará automáticamente porque el volumen de datos ya existe.

### 🛑 Limpieza Total (Reset Destructivo)
Este comando **detiene los servicios y elimina permanentemente todos los datos**:

```bash
docker-compose down -v
```

> ⚠️ **CUIDADO**: El flag `-v` borrará toda la información en la base de datos. Úsalo solo si quieres que `init.sql` se ejecute nuevamente desde cero.

### 🔄 Reconstrucción del Entorno
Después de la limpieza, levanta todo nuevamente para inicializar la estructura actualizada:

```bash
docker-compose up -d --build
```

---

## 🌍 Configuración Global (Timezone)

**CRÍTICO**: Todos los servicios usan la zona horaria del archivo `.env`:

```yaml
TZ: ${APP_TIMEZONE:-America/Guayaquil}
PGTZ: ${APP_TIMEZONE:-America/Guayaquil}  # PostgreSQL interno
```

Modifica `APP_TIMEZONE` en `.env` si necesitas otra zona horaria.

---

## 📚 Variables de Entorno (.env)

```env
# Base de datos
DB_HOST=database
DB_PORT=5432
DB_NAME=trabajos_db
DB_USER=postgres
DB_PASS=tu_contraseña

# Logs Service
LOGS_SERVICE_URL=http://logs_service:8000
LOGS_TIMEOUT=5

# Aplicación
APP_TIMEZONE=America/Guayaquil
```

---

## 📖 Convenciones de Logging

Los logs siguen este formato:
- **[IN]**: Iniciando una operación
- **[OUT]**: Datos extraídos exitosamente
- **[ERROR]**: Fallos y errores

Ejemplo:
```
[IN] Iniciando scraping en Grupo Palmon
[OUT] Extraído: Ingeniero de Sistemas | URL: https://...
[ERROR] Conexión rechazada por HiringRoom
```

---

## 🚀 Flujo de Ejecución del Scraper

1. **ScraperService** obtiene lista de empresas activas de PostgreSQL
2. Para cada empresa, invoca el **motor correspondiente** (ej: HiringRoomEngine)
3. El motor extrae vacantes como objetos `Vacante`
4. **PostgresRepository** guarda/actualiza vacantes (retorna "INSERT" o "UPDATE")
5. Vacantes no encontradas se marcan como inactivas
6. **HttpLoggerAdapter** registra todas las acciones en Logs Service

---

## 🔌 Agregar un Nuevo Portal de Empleo

1. Crear nuevo motor en `04_TrabajosWeb_Scraper/src/infrastructure/adapters/` (ej: `workday_engine.py`)
2. Implementar la interfaz `extraer(subdominio, proveedor) → List[Vacante]`
3. Inyectar logger en constructor:
   ```python
   def __init__(self, logger):
       self.logger = logger
   ```
4. Registrar en `main.py`:
   ```python
   motores = {
       'hiringroom': HiringRoomEngine(logger=logger),
       'workday': WorkdayEngine(logger=logger)  # Nuevo
   }
   ```
5. Agregar empresas a tabla `empresas` con `proveedor='workday'`

El servicio enrutará automáticamente las empresas al motor correcto.

---

## 🛠️ Tecnologías Utilizadas

| Componente | Tecnología | Versión |
|-----------|-----------|---------|
| Lenguaje (Scraper) | Python | 3.11-slim |
| Lenguaje (Logs) | Python | 3.11-slim |
| Automación Web | Selenium | - |
| API Rest (Logs) | FastAPI | - |
| Base de Datos | PostgreSQL | 16-Alpine |
| Frontend | Next.js | 16.1.6 |
| UI Framework | React | 19.2.3 |
| Orquestación | Docker Compose | 3.8 |

---

## ❓ Preguntas Frecuentes

**P: ¿Cómo agrego una nueva empresa a scrapear?**
R: Inserta un registro en la tabla `empresas` con `id_estado=1` (activo) y el `proveedor` correcto.

**P: ¿Puedo cambiar la zona horaria?**
R: Sí, modifica `APP_TIMEZONE` en `.env` y reinicia los servicios con `docker-compose down && docker-compose up -d`.

**P: ¿Qué pasa si cambio `init.sql`?**
R: Debes ejecutar `docker-compose down -v` para reinicializar la BD, ya que el volumen persiste cambios automáticamente.

---

**Última actualización**: Febrero 2026
# Copilot Instructions - TrabajosWeb Central

## Project Overview
**TrabajosWeb Central** is a multi-service job scraping platform using Docker Compose. It automates extraction of job vacancies from employment portals (HiringRoom) and centralizes them in PostgreSQL.

**Services:**
- **Scraper** (Python): Extracts job postings via Selenium + HiringRoom integration
- **Logs Service** (FastAPI): HTTP-based centralized logging at `http://logs_service:8000`
- **Frontend** (Next.js 16): React-based UI (currently minimal)
- **Database** (PostgreSQL 16): Single source of truth for job data

## Architecture & Design Patterns

### Service Communication
- **One-way HTTP**: Scraper → Logs Service (`POST /escribir-log`)
- **Database**: All services share PostgreSQL (`database` host in docker network)
- **Environment-based routing**: `.env` file controls DB credentials, timezone, service URLs

### Scraper Pattern: Dependency Injection + Adapters
The scraper follows **clean architecture** (domain/application/infrastructure layers):

```python
# main.py: Inject adapters into service
repo = PostgresVacanteRepository(Config.DB_PARAMS)
logger = HttpLoggerAdapter()
motores = {'hiringroom': HiringRoomEngine(logger=logger)}
service = ScraperService(motores, repo, logger)
service.ejecutar_ciclo_completo()
```

**Key pattern**: Engine implementations (e.g., `HiringRoomEngine`) are swappable via dictionary. The service is **engine-agnostic** and delegates scraping to injected motors.

### Data Flow
1. `ScraperService.ejecutar_ciclo_completo()` fetches active companies from DB
2. For each company, the configured engine (`HiringRoomEngine`) extracts vacancies as `Vacante` objects
3. `PostgresVacanteRepository.guardar()` returns "INSERT" or "UPDATE" action per vacancy
4. Deactivation logic: vacancies missing from current scrape are marked inactive
5. `HttpLoggerAdapter` logs all actions asynchronously to Logs Service

### Error Handling Convention
Use the `@gestionar_errores` decorator (defined in `infrastructure/utils.py`):

```python
from infrastructure.utils import gestionar_errores

@gestionar_errores(capa="Aplicacion")  # "capa" = layer name for logs
def ejecutar_ciclo_completo(self):
    # errors automatically logged via logger
```

## Critical Developer Workflows

### Quick Start
```bash
docker-compose up -d --build             # Build and start all services
docker logs -f trabajos_scraper          # Monitor scraper execution
docker exec -it trabajos_scraper python /app/src/main.py  # Manual execution
```

### Database Reset (Destructive!)
```bash
docker-compose down -v                   # Stop + delete volumes
docker-compose up -d --build             # Reinitialize from init.sql
```
⚠️ Flag `-v` deletes ALL data. Only use when schema changes require fresh initialization.

### Schema Changes
1. Modify `init.sql` with new columns/tables
2. Run `docker-compose down -v` to reset (loses all job data)
3. Rerun `docker-compose up -d --build` to apply changes
4. Resume scraping with manual execution

## Project-Specific Conventions

### Timezone Handling (CRITICAL)
Every service sets timezone explicitly via Docker Compose environment:
```yaml
environment:
  TZ: ${APP_TIMEZONE:-America/Guayaquil}
  PGTZ: ${APP_TIMEZONE:-America/Guayaquil}  # PostgreSQL internal
```
Default: `America/Guayaquil`. Override via `.env`.

### Logging Convention
Log messages format: `"[IN]" | "[OUT]" | "[ERROR]"` prefixes
- `[IN]`: Starting operation
- `[OUT]`: Extracted data
- `[ERROR]`: Failures

Example: `logger.registrar(f"WEB_{nombre_log}", f"[OUT] Extraído: {v.titulo}")`

### Company Configuration
Companies are stored in `empresas` table with:
- `nombre`: Display name
- `nombre_log`: Uppercase identifier for logs
- `subdominio`: HiringRoom subdomain (e.g., "grupopalmon")
- `proveedor`: Engine type (e.g., "hiringroom")
- `id_estado`: Status (1=Active, 0=Inactive)

Active companies are pulled dynamically; the service adapts without code changes.

### Vacante Model Fields
Core fields in `domain/models.py`:
- **Mandatory**: `titulo`, `url`, `identificador` (UUID from URL)
- **Scraping fields**: `ubicacion`, `area`, `modalidad`, `tipo_contrato`
- **System fields**: `id_empresa`, `empresa`, `fecha_extraccion`, `descripcion`

## Key File Map
- **`docker-compose.yml`**: Service orchestration, network config, volume mapping
- **`init.sql`**: Database schema initialization (only runs on first `up`)
- **`04_TrabajosWeb_Scraper/`**:
  - `src/domain/models.py`: `Vacante` dataclass
  - `src/application/scraper_service.py`: Orchestrator (fetches companies, calls engines)
  - `src/infrastructure/adapters/`: PostgreSQL repo, Logger adapter, HiringRoom engine
  - `src/infrastructure/config.py`: Environment-based config loader
- **`04_TrabajosWeb_Logs/main.py`**: FastAPI logging service (`POST /escribir-log`)
- **`04_TrabajosWeb_Frontend/src/`**: Next.js app (minimal setup)

## Adding a New Job Portal

1. Create new engine in `04_TrabajosWeb_Scraper/src/infrastructure/adapters/` (e.g., `workday_engine.py`)
2. Implement same interface as `HiringRoomEngine`: `extraer(subdominio, proveedor) → List[Vacante]`
3. Inject logger via constructor: `def __init__(self, logger)`
4. Register in `main.py`:
   ```python
   motores = {
       'hiringroom': HiringRoomEngine(logger=logger),
       'workday': WorkdayEngine(logger=logger)  # Add here
   }
   ```
5. Add companies to `empresas` table with `proveedor='workday'`

The service automatically routes companies to correct engines.

## Dependencies & Tools
- **Python**: 3.11-slim (Scraper & Logs)
- **Selenium**: Browser automation for HiringRoom extraction
- **FastAPI**: Logs service HTTP API
- **psycopg2**: PostgreSQL connectivity
- **Next.js 16.x / React 19**: Frontend (minimal usage)
- **Docker Compose 3.8**: Networking, volume management, environment injection

---

**Questions?** Refer to `readme.md` for command reference or explore service code following the architecture layers (domain → application → infrastructure).

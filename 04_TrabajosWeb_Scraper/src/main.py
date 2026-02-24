from infrastructure.config import Config
from infrastructure.adapters.postgres_repository import PostgresVacanteRepository
from infrastructure.adapters.http_logger import HttpLoggerAdapter
from infrastructure.adapters.selenium_engine import SeleniumEngine # (Tu lógica de Selenium)
from application.scraper_service import ScraperService

if __name__ == "__main__":
    # 1. Preparar adaptadores
    repo = PostgresVacanteRepository(Config.DB_PARAMS)
    logger = HttpLoggerAdapter()
    engine = SeleniumEngine() # Debes mover tu lógica de driver.get aquí

    # 2. Inyectar en el servicio
    service = ScraperService(engine, repo, logger)

    # 3. Ejecutar
    service.procesar_empresa("PALMON", "https://grupopalmon.hiringroom.com")
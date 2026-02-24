from infrastructure.config import Config
from infrastructure.adapters.postgres_repository import PostgresVacanteRepository
from infrastructure.adapters.http_logger import HttpLoggerAdapter
from infrastructure.adapters.hiring_room_engine import HiringRoomEngine
from application.scraper_service import ScraperService

if __name__ == "__main__":
    # 1. Preparar adaptadores de infraestructura
    # El repositorio ahora tiene el método para consultar la lista de empresas
    repo = PostgresVacanteRepository(Config.DB_PARAMS)
    logger = HttpLoggerAdapter()

    # 2. Definir los motores disponibles (Estrategias)
    # Aquí es donde el comportamiento varía según el proveedor
    motores = {
        'hiringroom': HiringRoomEngine()
        # Cuando tengas otro, simplemente lo agregas aquí:
        # 'workday': WorkdayEngine() 
    }

    # 3. Inyectar el mapa de motores en el servicio
    # El servicio ahora es un orquestador dinámico
    service = ScraperService(motores, repo, logger)

    # 4. Ejecutar el flujo global
    # Ya no le pasamos una empresa fija, él consulta la BD y procesa todas las activas
    service.ejecutar_ciclo_completo()
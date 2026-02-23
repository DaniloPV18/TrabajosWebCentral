from infrastructure.file_manager import FileHandlerAdapter
from schemas.log_schema import LogRequest

class LoggerService:
    def __init__(self):
        self.adapter = FileHandlerAdapter()

    def execute_logging(self, data: LogRequest):
        # CORRECCIÓN: Usa 'data.nombre_log' en lugar de 'name'
        clean_name = data.nombre_log.strip()
        
        # Ahora el adaptador recibirá "WEB_PALMON" tal cual
        logger = self.adapter.get_logger(clean_name)
        
        # Mapeo de niveles
        if data.nivel == "ERROR":
            logger.error(data.mensaje)
        elif data.nivel == "WARNING":
            logger.warning(data.mensaje)
        else:
            logger.info(data.mensaje)
import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

class FileHandlerAdapter:
    BASE_STORAGE_PATH = "/app/storage"

    @staticmethod
    def _custom_namer(name):
        """
        Transforma el nombre de rotación estándar de Python:
        'archivo.log.1' -> 'archivo_01.log'
        """
        if ".log." in name:
            base_path, number = name.split(".log.")
            return f"{base_path}_{int(number):02d}.log"
        return name

    @classmethod
    def _get_subfolder(cls, base_name: str) -> str:
        """ Clasifica los logs en carpetas según su prefijo """
        nombre_upper = base_name.upper()
        if "WEB_" in nombre_upper:
            return "scraping"
        if "BD_" in nombre_upper:
            return "database"
        return "others"

    @classmethod
    def get_logger(cls, base_name: str):
        fecha_hoy = datetime.now().strftime("%d-%m-%Y")
        subfolder = cls._get_subfolder(base_name)
        
        folder_path = os.path.join(cls.BASE_STORAGE_PATH, subfolder)
        os.makedirs(folder_path, exist_ok=True)

        # Nombre del archivo principal (siempre el actual)
        nombre_archivo = f"{base_name}-{fecha_hoy}.log"
        ruta_completa = os.path.join(folder_path, nombre_archivo)

        logger = logging.getLogger(nombre_archivo)
        
        # Evita duplicar handlers si el servicio permanece activo
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            
            # delay=True es CRÍTICO para evitar bloqueos en Windows/Docker
            handler = RotatingFileHandler(
                ruta_completa, 
                maxBytes=10485760, # 10MB
                backupCount=100,
                encoding='utf-8',
                delay=True 
            )

            handler.namer = cls._custom_namer
            
            formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
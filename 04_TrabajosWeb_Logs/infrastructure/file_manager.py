import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

class FileHandlerAdapter:
    BASE_STORAGE_PATH = "/app/storage"

    @classmethod
    def get_logger(cls, base_name: str):
        fecha_hoy = datetime.now().strftime("%d-%m-%Y")
        
        # Usamos upper() solo para la lógica de carpetas
        nombre_check = base_name.upper()
        
        if "WEB_" in nombre_check:
            subfolder = "scraping"
        elif "BD_" in nombre_check:
            subfolder = "database"
        else:
            subfolder = "others"

        # # Crear la ruta física
        # folder_path = os.path.join(cls.BASE_STORAGE_PATH, subfolder)
        # if not os.path.exists(folder_path):
        #     os.makedirs(folder_path)
        # Construcción de ruta física
        folder_path = os.path.join(cls.BASE_STORAGE_PATH, subfolder)
        os.makedirs(folder_path, exist_ok=True)

        nombre_archivo = f"{base_name}-{fecha_hoy}.log"
        ruta_completa = os.path.join(folder_path, nombre_archivo)

        logger = logging.getLogger(nombre_archivo)
        
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            # Rotación de 10MB independiente por archivo
            handler = RotatingFileHandler(
                ruta_completa, 
                maxBytes=10485760, # 10MB
                backupCount=5,
                encoding='utf-8'
            )
            formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
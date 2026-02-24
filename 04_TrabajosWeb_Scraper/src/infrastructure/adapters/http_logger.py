import requests
from datetime import datetime
from domain.ports import LoggerPort
from infrastructure.config import Config # Importamos nuestra clase de config

class HttpLoggerAdapter(LoggerPort):
    def __init__(self):
        # La URL se carga una sola vez al instanciar el adaptador
        self.url = Config.LOGS_SERVICE_URL
        self.timeout = Config.LOGS_TIMEOUT

    def registrar(self, nombre_log, mensaje, nivel="INFO"):
        ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
        mensaje_formateado = f" {mensaje}"
        
        payload = {
            "nombre_log": nombre_log, 
            "nivel": nivel, 
            "mensaje": mensaje_formateado
        }

        try:
            # Cero constantes "hardcodeadas" aquí
            requests.post(self.url, json=payload, timeout=self.timeout)
        except Exception as e:
            # Seguimos usando print aquí para evitar recursión si el MS de logs falla
            print(f"[SISTEMA CRITICAL] Fallo conexión a MS LOGS ({self.url}): {str(e)}")
            print(f"MENSAJE PERDIDO: {mensaje_formateado}")
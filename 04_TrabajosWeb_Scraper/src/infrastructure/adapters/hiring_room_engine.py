from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from domain.models import Vacante
from domain.ports import ScraperEngine
from infrastructure.utils import gestionar_errores
import time
import re # Usaremos regex para extraer el UUID de forma segura

class HiringRoomEngine(ScraperEngine):
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")

    @gestionar_errores(capa="Infraestructura_Web")
    def extraer(self, subdominio) -> list:
        url_final = f"https://{subdominio}.hiringroom.com/jobs"
        
        driver = webdriver.Chrome(options=self.options)
        vacantes_modelos = []
        
        try:
            driver.get(url_final)
            time.sleep(5) 
            
            contenedor = driver.find_element(By.CLASS_NAME, "vacancyDataContainer")
            enlaces = contenedor.find_elements(By.TAG_NAME, "a")

            for enlace in enlaces:
                url = enlace.get_attribute("href") # Ejemplo: https://empresa.hiringroom.com/jobs/get_vacancy/uuid-123
                
                # --- Lógica de Extracción por Posición ---
                # Dividimos la URL por los slashes y tomamos el último elemento
                partes_url = url.strip('/').split('/')
                identificador = partes_url[-1] if partes_url else url
                # -----------------------------------------

                try:
                    texto_card = enlace.find_element(By.CLASS_NAME, "card").text
                    titulo = texto_card.split('\n')[0] if texto_card else "Sin Título"
                except:
                    titulo = "Sin Título"
                
                vacantes_modelos.append(Vacante(
                    titulo=titulo,
                    url=url,
                    identificador=identificador # Ahora guarda solo el UUID (ej: uuid-123)
                ))
        finally:
            driver.quit()
            
        return vacantes_modelos
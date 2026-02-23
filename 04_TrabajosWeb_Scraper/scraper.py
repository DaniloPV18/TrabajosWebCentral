import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from utils import registrar_log, controlar_errores_centralizado, guardar_vacante

class HiringRoomScraper:
    def __init__(self, empresa_nombre):
        self.empresa_nombre = empresa_nombre.upper() # Opcional: forzar empresa en mayúsculas
        # Esto generará: WEB_PALMON y BD_PALMON
        self.log_web = f"WEB_{self.empresa_nombre}"
        self.log_bd = f"BD_{self.empresa_nombre}"
        
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.driver = None

    def iniciar_driver(self):
        self.driver = webdriver.Chrome(options=self.options)

    @controlar_errores_centralizado
    def ejecutar(self, url_base):
        # --- WEB LOG: IN ---
        registrar_log(self.log_web, f"--- [IN] Iniciando petición a: {url_base}/jobs ---")
        self.iniciar_driver()
        
        try:
            self.driver.get(f"{url_base}/jobs")
            time.sleep(5) 
            
            contenedor = self.driver.find_element(By.CLASS_NAME, "vacancyDataContainer")
            enlaces_vacantes = contenedor.find_elements(By.TAG_NAME, "a")
            
            registrar_log(self.log_web, f"Conexión exitosa. Elementos detectados: {len(enlaces_vacantes)}")

            for enlace in enlaces_vacantes:
                # --- WEB LOG: OUT (Extracción de datos) ---
                url_relativa = enlace.get_attribute("href")
                titulo = enlace.find_element(By.CLASS_NAME, "card").text.split('\n')[0]
                
                registrar_log(self.log_web, f"[OUT] Extraído: {titulo} | URL: {url_relativa}")
                
                # --- BD LOG: Gestión de datos ---
                guardar_vacante(self.log_bd, titulo, self.empresa_nombre, url_relativa)
                
            registrar_log(self.log_web, f"--- [FIN WEB] Proceso completado para {self.empresa_nombre} ---")
            
        finally:
            if self.driver:
                self.driver.quit()
                
if __name__ == "__main__":
    # Scraper para la empresa A
    scraper_a = HiringRoomScraper("PALMON")
    scraper_a.ejecutar("https://grupopalmon.hiringroom.com")

    # # Scraper para la empresa B
    # scraper_b = HiringRoomScraper("otra_empresa")
    # scraper_b.ejecutar("https://otraempresa.hiringroom.com")
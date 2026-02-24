# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from domain.models import Vacante
# from infrastructure.utils import gestionar_errores
# import time

# class SeleniumEngine:
#     def __init__(self):
#         self.options = Options()
#         self.options.add_argument("--headless")
#         self.options.add_argument("--no-sandbox")
#         self.options.add_argument("--disable-dev-shm-usage")

#     @gestionar_errores(capa="Infraestructura_Web")
#     def extraer(self, url_base) -> list:
#         # Iniciamos el driver (El decorador atrapará si falta el binario de Chrome)
#         driver = webdriver.Chrome(options=self.options)
#         vacantes_modelos = []
        
#         try:
#             driver.get(f"{url_base}/jobs")
#             time.sleep(5) # Considera usar WebDriverWait para algo más pro
            
#             contenedor = driver.find_element(By.CLASS_NAME, "vacancyDataContainer")
#             enlaces = contenedor.find_elements(By.TAG_NAME, "a")

#             for enlace in enlaces:
#                 url = enlace.get_attribute("href")
#                 # Extraemos el título limpiando ruidos
#                 text_content = enlace.find_element(By.CLASS_NAME, "card").text
#                 titulo = text_content.split('\n')[0] if text_content else "Sin Título"
                
#                 # Instanciamos el modelo de dominio
#                 vacantes_modelos.append(Vacante(
#                     titulo=titulo,
#                     url=url,
#                     identificador=url,
#                     empresa="" 
#                 ))
#         finally:
#             driver.quit()
            
#         return vacantes_modelos
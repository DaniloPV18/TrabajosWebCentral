from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from domain.models import Vacante
from domain.ports import ScraperEngine
from infrastructure.utils import gestionar_errores
import time

class HiringRoomEngine(ScraperEngine):
    def __init__(self, logger):
        self.options = Options()
        self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.logger = logger

    @gestionar_errores(capa="Infraestructura_Web")
    def extraer(self, subdominio, proveedor) -> list:
        url_final = f"https://{subdominio}.hiringroom.com/jobs"
        driver = webdriver.Chrome(options=self.options)
        vacantes_modelos = []
        
        try:
            driver.get(url_final)
            time.sleep(7) 
            
            contenedor = driver.find_element(By.CLASS_NAME, "vacancyDataContainer")
            enlaces = contenedor.find_elements(By.TAG_NAME, "a")

            for enlace in enlaces:
                url = enlace.get_attribute("href")
                partes_url = url.strip('/').split('/')
                identificador = partes_url[-1] if partes_url else url

                # 1. Título
                try:
                    titulo = enlace.find_element(By.CLASS_NAME, "name__vacancy").text.strip()
                except:
                    try:
                        titulo = enlace.find_element(By.TAG_NAME, "h4").text.strip()
                    except:
                        titulo = "Título no encontrado"

                # 2. Ubicación
                try:
                    ubicacion = enlace.find_element(By.XPATH, ".//span[i[contains(@class, 'hr-Location-pin')]]").text.strip()
                except:
                    ubicacion = "No especificada"

                # 3. Área
                try:
                    area = enlace.find_element(By.XPATH, ".//span[i[contains(@class, 'hr-Work-area')]]").text.strip()
                except:
                    area = "No especificada"

                # 4. Tags Dinámicos (Clasificación por Icono)
                tipo_contrato = "No especificado"
                modalidad = "No especificado"
                
                try:
                    # Obtenemos los contenedores de etiquetas
                    tags_elements = enlace.find_elements(By.CLASS_NAME, "tag-vacancy")
                    
                    for tag in tags_elements:
                        texto_tag = tag.text.strip()
                        if not texto_tag: continue
                        
                        try:
                            # Buscamos el icono dentro del tag para saber qué dato es
                            icono = tag.find_element(By.TAG_NAME, "i")
                            clase_icono = icono.get_attribute("class")
                            
                            # Si el icono es el reloj, es información de Contrato
                            if "hr-Clock" in clase_icono:
                                tipo_contrato = texto_tag
                            # Si es el de empresa (o cualquier otro), es Modalidad
                            elif "hr-Company" in clase_icono:
                                modalidad = texto_tag
                            else:
                                # Si no coincide con los anteriores pero hay texto, 
                                # lo mantenemos como modalidad por ser el campo restante
                                modalidad = texto_tag
                        except:
                            # Si no hay icono pero hay texto (caso raro), asignar a modalidad
                            modalidad = texto_tag
                except Exception as e:
                    self.logger.registrar(f"WEB_PR_{proveedor}", f"Error en tags: {str(e)}", "WARNING")

                # --- LOGS DETALLADOS ---
                self.logger.registrar(f"WEB_PR_{proveedor}", f"V_ENCONTRADA: {subdominio.upper()}", "INFO")
                self.logger.registrar(f"WEB_PR_{proveedor}", f"  |-- TITULO: {titulo}", "INFO")
                self.logger.registrar(f"WEB_PR_{proveedor}", f"  |-- ÁREA: {area}", "INFO")
                self.logger.registrar(f"WEB_PR_{proveedor}", f"  |-- UBICACIÓN: {ubicacion}", "INFO")
                self.logger.registrar(f"WEB_PR_{proveedor}", f"  |-- CONTRATO: {tipo_contrato} | MODALIDAD: {modalidad}", "INFO")
                self.logger.registrar(f"WEB_PR_{proveedor}", "-"*40, "INFO")

                vacantes_modelos.append(Vacante(
                    titulo=titulo,
                    url=url,
                    identificador=identificador,
                    ubicacion=ubicacion,
                    area=area,
                    modalidad=modalidad,
                    tipo_contrato=tipo_contrato
                ))
        finally:
            driver.quit()
            
        return vacantes_modelos
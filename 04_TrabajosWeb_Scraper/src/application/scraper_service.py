from infrastructure.utils import gestionar_errores

class ScraperService:
    def __init__(self, motores_dict, repository, logger):
        """
        motores_dict: Un diccionario {'hiringroom': HiringRoomEngine()}
        """
        self.motores = motores_dict
        self.repository = repository
        self.logger = logger

    @gestionar_errores(capa="Aplicacion")
    def ejecutar_ciclo_completo(self):
        # 1. CONSULTO: Trae la lista de empresas de la BD
        empresas = self.repository.obtener_empresas_configuradas()
        
        if not empresas:
            self.logger.registrar("SISTEMA", "No hay empresas activas para procesar", "WARNING")
            return

        for id_emp, nombre, nombre_log, subdominio, proveedor in empresas:
            # 2. SELECCIONO EL COMPORTAMIENTO: Buscamos el motor por nombre de proveedor
            motor = self.motores.get(proveedor.lower())
            
            if not motor:
                self.logger.registrar(f"WEB_{nombre_log}", f"Proveedor '{proveedor}' no implementado", "ERROR")
                continue

            self.logger.registrar(f"WEB_{nombre_log}", f"--- [IN] Iniciando scraping en {subdominio} ---")
            
            # 3. LEO: El motor hace su trabajo sucio con Selenium
            vacantes_encontradas = motor.extraer(subdominio, proveedor)
            
            self.logger.registrar(f"WEB_{nombre_log}", f"Conexión exitosa. Detectados: {len(vacantes_encontradas)}")
            
            # 4. REGISTRO: Procesado transparente (idéntico para todos los proveedores)
            for v in vacantes_encontradas:
                v.empresa = nombre
                v.id_empresa = id_emp # FK para la base de datos
                
                self.logger.registrar(f"WEB_{nombre_log}", v.a_formato_log())
                
                # Guardado en base de datos con el repositorio
                exito = self.repository.guardar(v)
                
                prefijo = "[INSERT]" if exito else "[SKIP]"
                self.logger.registrar(f"BD_{nombre_log}", f"{prefijo} {v.titulo}")
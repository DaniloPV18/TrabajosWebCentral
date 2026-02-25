from infrastructure.utils import gestionar_errores

class ScraperService:
    def __init__(self, motores_dict, repository, logger):
        self.motores = motores_dict
        self.repository = repository
        self.logger = logger

    @gestionar_errores(capa="Aplicacion")
    def ejecutar_ciclo_completo(self):
        # 1. Trae la lista de empresas de la BD
        empresas = self.repository.obtener_empresas_configuradas()
        
        if not empresas:
            self.logger.registrar("SISTEMA", "No hay empresas activas para procesar", "WARNING")
            return

        for id_emp, nombre, nombre_log, subdominio, proveedor in empresas:
            motor = self.motores.get(proveedor.lower())
            
            if not motor:
                self.logger.registrar(f"WEB_{nombre_log}", f"Proveedor '{proveedor}' no implementado", "ERROR")
                continue

            self.logger.registrar(f"WEB_{nombre_log}", f"--- [IN] Iniciando scraping en {nombre} ---")
            
            # 2. El motor extrae las vacantes actuales
            vacantes_encontradas = motor.extraer(subdominio, proveedor)
            
            self.logger.registrar(f"WEB_{nombre_log}", f"Conexión exitosa. Detectados: {len(vacantes_encontradas)}")
            
            # --- BLOQUE DE SIMULACIÓN PARA PRUEBA ---
            if len(vacantes_encontradas) > 3:
                self.logger.registrar(f"WEB_{nombre_log}", "SIMULACIÓN: Eliminando 3 vacantes de la lista para probar desactivación", "WARNING")
                # Quitamos las 3 últimas vacantes encontradas
                vacantes_encontradas = vacantes_encontradas[:-3]
            # ----------------------------------------
            
            # 3. Lista para rastrear qué vacantes siguen vivas en la web
            ids_vivos = []
            
            # ... (dentro del bucle for v in vacantes_encontradas)
            for v in vacantes_encontradas:
                v.empresa = nombre
                v.id_empresa = id_emp 
                
                ids_vivos.append(v.identificador)
                
                # Aquí recibimos "INSERT" o "UPDATE" directamente desde el repo
                resultado_accion = self.repository.guardar(v)
                
                self.logger.registrar(f"WEB_{nombre_log}", v.a_formato_log())
                
                # Imprimimos el resultado real de la BD
                self.logger.registrar(f"BD_{nombre_log}", f"UUID:{v.identificador} | [{resultado_accion}] {v.titulo}")

            # 4. CONTROL DE DESACTIVACIÓN: Sincronizamos el estado de la BD con la realidad de la web
            if ids_vivos:
                # Ahora 'titulos_desactivados' es una lista de nombres
                titulos_desactivados = self.repository.desactivar_vacantes_no_listadas(id_emp, ids_vivos)
                
                if titulos_desactivados:
                    self.logger.registrar(f"BD_{nombre_log}", f"[CLEANUP] Se desactivaron {len(titulos_desactivados)} vacantes:", "INFO")
                    
                    # Imprimimos cada vacante dada de baja
                    for titulo_old in titulos_desactivados:
                        self.logger.registrar(f"BD_{nombre_log}", f"UUID:{v.identificador} | [OFFLINE] -> {titulo_old}", "WARNING")
                else:
                    self.logger.registrar(f"BD_{nombre_log}", "[CLEANUP] Sin cambios: Todas las vacantes siguen vigentes.", "DEBUG")
            
            self.logger.registrar(f"WEB_{nombre_log}", f"--- [OUT] Fin de ciclo para {nombre} ---")
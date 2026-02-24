from infrastructure.utils import gestionar_errores

class ScraperService:
    def __init__(self, scraper_engine, repository, logger):
        self.scraper_engine = scraper_engine
        self.repository = repository
        self.logger = logger

    @gestionar_errores(capa="Aplicacion")
    def procesar_empresa(self, nombre_empresa, url_base):
        # Si algo falla aquí adentro, el decorador lo captura automáticamente
        self.logger.registrar(f"WEB_{nombre_empresa}", f"--- [IN] Iniciando petición a: {url_base}")
        
        vacantes_encontradas = self.scraper_engine.extraer(url_base)
        self.logger.registrar(f"WEB_{nombre_empresa}", f"Conexión exitosa. Elementos detectados: {len(vacantes_encontradas)}")
        
        for v in vacantes_encontradas:
            v.empresa = nombre_empresa
            
            # Log de la vacante usando el método del modelo que creamos
            self.logger.registrar(f"WEB_{nombre_empresa}", v.a_formato_log())            
            
            # Intento de guardado
            exito = self.repository.guardar(v)
            
            prefijo = "[INSERT]" if exito else "[SKIP]"
            self.logger.registrar(f"BD_{nombre_empresa}", f"{prefijo} {v.titulo}")
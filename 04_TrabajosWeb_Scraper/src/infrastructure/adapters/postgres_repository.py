import psycopg2
from domain.ports import VacanteRepository
from infrastructure.utils import gestionar_errores

class PostgresVacanteRepository(VacanteRepository):
    def __init__(self, db_config):
        self.config = db_config

    @gestionar_errores(capa="Infraestructura")
    def guardar(self, vacante) -> bool:
        # 1. Agregamos las 4 nuevas columnas al query
        query = """
            INSERT INTO vacantes (
                titulo, identificador, url, id_empresa, 
                ubicacion, area, modalidad, tipo_contrato, id_estado
            )
            VALUES (
                %s, %s, %s, %s, 
                %s, %s, %s, %s, 
                (SELECT id FROM estado WHERE nombre = 'Activo' LIMIT 1)
            )
            ON CONFLICT (identificador) DO NOTHING;
        """        
        # 2. Mapeamos los nuevos atributos del modelo Vacante
        params = (
            vacante.titulo, 
            vacante.identificador, 
            vacante.url, 
            vacante.id_empresa,
            vacante.ubicacion,     # <--- Nuevo
            vacante.area,          # <--- Nuevo
            vacante.modalidad,     # <--- Nuevo
            vacante.tipo_contrato  # <--- Nuevo
        )
        with psycopg2.connect(**self.config) as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                conn.commit()
                return cur.rowcount > 0
    
    @gestionar_errores(capa="Infraestructura")      
    def obtener_empresas_configuradas(self):
        # 3. Aseguramos que el query use el nombre de columna id_estado (con guion bajo)
        query = "SELECT id, nombre, nombre_log, subdominio, proveedor FROM empresas WHERE id_estado = 1;"
        with psycopg2.connect(**self.config) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchall()
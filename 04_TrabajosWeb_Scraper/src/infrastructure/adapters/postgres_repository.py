import psycopg2
from domain.ports import VacanteRepository
from infrastructure.utils import gestionar_errores

class PostgresVacanteRepository(VacanteRepository):
    def __init__(self, db_config):
        self.config = db_config

    @gestionar_errores(capa="Infraestructura")
    def guardar(self, vacante) -> str:
        # Usamos xmax: si es 0 significa que se insertó una nueva fila.
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
            ON CONFLICT (identificador) DO UPDATE SET
                titulo = EXCLUDED.titulo,
                ubicacion = EXCLUDED.ubicacion,
                area = EXCLUDED.area,
                modalidad = EXCLUDED.modalidad,
                tipo_contrato = EXCLUDED.tipo_contrato,
                fecha_actualizado = CURRENT_TIMESTAMP,
                id_estado = (SELECT id FROM estado WHERE nombre = 'Activo' LIMIT 1)
            RETURNING (xmax = 0) AS es_nuevo;
        """        
        params = (
            vacante.titulo, 
            vacante.identificador, 
            vacante.url, 
            vacante.id_empresa,
            vacante.ubicacion,
            vacante.area,
            vacante.modalidad,
            vacante.tipo_contrato
        )
        with psycopg2.connect(**self.config) as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                resultado = cur.fetchone()
                conn.commit()
                
                if resultado is not None:
                    return "INSERT" if resultado[0] else "UPDATE"
                return "SKIP"
    
    @gestionar_errores(capa="Infraestructura")      
    def obtener_empresas_configuradas(self):
        # 3. Aseguramos que el query use el nombre de columna id_estado (con guion bajo)
        query = "SELECT id, nombre, nombre_log, subdominio, proveedor FROM empresas WHERE id_estado = 1;"
        with psycopg2.connect(**self.config) as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                return cur.fetchall()
            
    @gestionar_errores(capa="Infraestructura")
    def desactivar_vacantes_no_listadas(self, id_empresa, identificadores_activos):
        if not identificadores_activos:
            return []

        # Usamos RETURNING titulo para saber cuáles se desactivaron
        query = """
            UPDATE vacantes 
            SET id_estado = (SELECT id FROM estado WHERE nombre = 'Inactivo' LIMIT 1),
                fecha_actualizado = CURRENT_TIMESTAMP
            WHERE id_empresa = %s 
              AND identificador NOT IN %s
              AND id_estado = (SELECT id FROM estado WHERE nombre = 'Activo' LIMIT 1)
            RETURNING titulo;
        """
        
        with psycopg2.connect(**self.config) as conn:
            with conn.cursor() as cur:
                cur.execute(query, (id_empresa, tuple(identificadores_activos)))
                # Obtenemos todos los títulos afectados
                filas_afectadas = cur.fetchall()
                conn.commit()
                # Retornamos una lista simple de strings (títulos)
                return [fila[0] for fila in filas_afectadas]
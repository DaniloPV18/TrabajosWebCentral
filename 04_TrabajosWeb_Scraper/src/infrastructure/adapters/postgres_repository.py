import psycopg2
from domain.ports import VacanteRepository
from infrastructure.utils import gestionar_errores

class PostgresVacanteRepository(VacanteRepository):
    def __init__(self, db_config):
        self.config = db_config

    @gestionar_errores(capa="Infraestructura")
    def guardar(self, vacante) -> bool:
        query = """
            INSERT INTO Vacantes (Titulo, Identificador, Url, IDEstado)
            VALUES (%s, %s, %s, (SELECT id FROM Estado WHERE Nombre = 'Activo' LIMIT 1))
            ON CONFLICT (Identificador) DO NOTHING;
        """
        # Ya no necesitamos el try-except manual, el decorador lo hace por nosotros
        with psycopg2.connect(**self.config) as conn:
            with conn.cursor() as cur:
                # Nota: corregí el envío de parámetros según tu query
                cur.execute(query, (vacante.titulo, vacante.identificador, vacante.url))
                conn.commit()
                return cur.rowcount > 0
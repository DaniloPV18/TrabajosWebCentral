import os
import psycopg2
import requests
import functools
from dotenv import load_dotenv

load_dotenv()

def controlar_errores_centralizado(funcion):
    @functools.wraps(funcion)
    def wrapper(*args, **kwargs):
        try:
            return funcion(*args, **kwargs)
        except Exception as e:
            error_msg = f"Error en {funcion.__name__}: {str(e)}"
            registrar_log(error_msg, "ERROR")
            return None
    return wrapper

def registrar_log(nombre_log, mensaje, nivel="INFO"):
    """
    Envía un registro al servicio de logs centralizado.
    nombre_log: El nombre del archivo (ej: 'scraper_palmon')
    """
    url = "http://logs_service:8000/escribir-log"
    payload = {
        "nombre_log": nombre_log,
        "nivel": nivel,
        "mensaje": mensaje
    }
    try:
        requests.post(url, json=payload, timeout=2)
    except Exception:
        # Si el servicio de logs falla, imprimimos en consola del contenedor
        print(f"FALLO LOG [{nombre_log}]: {mensaje}")

def obtener_conexion():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        port=os.getenv("DB_PORT")
    )
    
def guardar_vacante(nombre_log_bd, titulo, empresa, url):
    try:
        with obtener_conexion() as conn:
            with conn.cursor() as cur:
                # Intento de inserción
                cur.execute("""
                    INSERT INTO vacantes (titulo, empresa, url_vacante)
                    VALUES (%s, %s, %s) ON CONFLICT (url_vacante) DO NOTHING
                """, (titulo, empresa, url))
                conn.commit()
                
                # Registro en Log de BD
                if cur.rowcount > 0:
                    registrar_log(nombre_log_bd, f"[INSERT] Nueva vacante: {titulo}")
                else:
                    registrar_log(nombre_log_bd, f"[SKIP] Ya existente: {titulo}")
                    
    except Exception as e:
        registrar_log(nombre_log_bd, f"[ERROR BD] Fallo al procesar {titulo}: {str(e)}", "ERROR")

@controlar_errores_centralizado
def crear_tabla_vacantes():
    with obtener_conexion() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS vacantes (
                    id SERIAL PRIMARY KEY,
                    titulo VARCHAR(255),
                    empresa VARCHAR(255),
                    url_vacante TEXT UNIQUE,
                    fecha_extraccion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()
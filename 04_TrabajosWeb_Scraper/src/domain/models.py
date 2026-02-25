from dataclasses import dataclass
from datetime import datetime

@dataclass
class Vacante:
    # 1. Campos Obligatorios (Sin valor por defecto)
    titulo: str
    url: str
    identificador: str 
    
    # 2. Nuevos campos de Scraping (Con valor por defecto)
    ubicacion: str = "No especificada"
    area: str = "No especificada"
    modalidad: str = "No especificada"
    tipo_contrato: str = "No especificado"
    
    # 3. Campos de Gestión y Metadatos
    id_empresa: int = None
    empresa: str = ""
    descripcion: str = ""
    fecha_extraccion: datetime = None

    def a_formato_log(self) -> str:
        """Devuelve la representación para los logs de scraping."""
        return f"[OUT] Extraído: {self.titulo} | URL: {self.url}"
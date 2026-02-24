from dataclasses import dataclass
from datetime import datetime

@dataclass
class Vacante:
    titulo: str
    url: str
    identificador: str  # La URL suele ser el identificador único
    
    id_empresa: int = None  # <-- Campo nuevo para la FK de la base de datos
    empresa: str = ""
    
    descripcion: str = ""
    fecha_extraccion: datetime = None

    def a_formato_log(self) -> str:
        """Devuelve la representación para los logs de scraping."""
        return f"[OUT] Extraído: {self.titulo} | URL: {self.url}"
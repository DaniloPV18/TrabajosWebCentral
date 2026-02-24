from dataclasses import dataclass
from datetime import datetime

@dataclass
class Vacante:
    titulo: str
    url: str
    empresa: str
    identificador: str  # La URL suele ser el identificador único
    descripcion: str = ""
    fecha_extraccion: datetime = None

    def a_formato_log(self) -> str:
        """Devuelve la representación para los logs de scraping."""
        return f"[OUT] Extraído: {self.titulo} | URL: {self.url}"
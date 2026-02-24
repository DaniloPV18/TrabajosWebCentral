from abc import ABC, abstractmethod

class VacanteRepository(ABC):
    @abstractmethod
    def guardar(self, vacante) -> bool:
        """Guarda una vacante en la persistencia."""
        pass

class LoggerPort(ABC):
    @abstractmethod
    def registrar(self, nombre_log: str, mensaje: str, nivel: str = "INFO"):
        """Envía un registro al sistema de logs."""
        pass
    
class ScraperEngine(ABC):
    @abstractmethod
    def extraer(self, subdominio: str) -> list:
        """Debe retornar una lista de objetos Vacante"""
        pass
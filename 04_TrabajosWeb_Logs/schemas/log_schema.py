from pydantic import BaseModel
from typing import Literal

class LogRequest(BaseModel):
    nombre_log: str
    nivel: Literal["INFO", "ERROR", "WARNING"]
    mensaje: str
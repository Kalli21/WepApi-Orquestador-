from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ComentarioDTO(BaseModel):
    id: Optional[int] = None
    correlativo: Optional[int] = None
    contenido: Optional[str] = None
    fecha: Optional[str] = None
    producto: Optional[str] = None
    cliente: Optional[str] = None
    tema: Optional[int] = None
    sentimiento: Optional[str] = None
    probabilidad: Optional[List[float]] = []
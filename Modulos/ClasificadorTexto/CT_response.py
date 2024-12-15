from pydantic import BaseModel
from typing import List, Optional, Any

# Modelo para estructurar la respuesta del servicio .NET
class RelacionComCat(BaseModel):
    correlativo: Optional[int] = None
    idComentario: Optional[int] = None	
    idCategoria: Optional[int] = None	
    nombreCategoria: Optional[str] = None	
    nombreProducto: Optional[str] = None	
    codCliente: Optional[str] = None	
    text: Optional[str] = None	
    robabilidades: Optional[List[float]] = None	
    categoria: Optional[int] = None	
    fecha: Optional[str] = None

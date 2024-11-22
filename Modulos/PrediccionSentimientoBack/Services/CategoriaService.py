
from fastapi import  HTTPException

from .HttpConsult import HttpConsult
from ..PS_response import PS_Response
from ..PS_request import Categoria

class CategoriaService(HttpConsult):
    
    async def crear_categoria(self, categoria: Categoria) -> PS_Response:
        
        try:      
            url = "/Categoria"        
            return await self._send_request(url, "post", categoria)       

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
        
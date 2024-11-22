
from fastapi import  HTTPException

from .HttpConsult import HttpConsult
from ..PS_response import PS_Response
from ..PS_request import Comentario

class ComentarioService(HttpConsult):

    async def crear_comentario(self,comentario: Comentario) -> PS_Response:
        
        try:       
            url = "/Comentario"        
            return await self._send_request(url, "post", comentario)       

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")





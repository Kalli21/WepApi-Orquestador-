
from fastapi import  HTTPException

from .HttpConsult import HttpConsult
from ..PS_response import PS_Response
from ..PS_request import Comentario, PS_ComentariosFiltros

class ComentarioService(HttpConsult):

    async def crear_comentario(self,comentario: Comentario) -> PS_Response:
        
        try:       
            url = "/Comentario"        
            return await self._send_request(url, "post", comentario)       

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")


    

    async def get_comentarios_min_info(self, filtro: PS_ComentariosFiltros) -> PS_Response:
            
            try:       
                url = "/Comentario/username"        
                return await self._send_request(url, "post", filtro)       

            except ValueError as exc:
                raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
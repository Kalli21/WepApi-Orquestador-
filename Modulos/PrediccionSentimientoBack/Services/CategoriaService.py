
from fastapi import  HTTPException

from .HttpConsult import HttpConsult
from ..PS_response import PS_Response
from ..PS_request import Categoria, PS_CategoriasFiltros


class CategoriaService(HttpConsult):
    
    async def crear_categoria(self, categoria: Categoria) -> PS_Response:
        
        try:      
            url = "/Categoria"        
            return await self._send_request(url, "post", categoria)       

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
        
    async def get_categorias_by_user_con_comentarios(self,user_name , filtros: PS_CategoriasFiltros) -> PS_Response:
        
        try:      
            url = f"/Categoria/username/coment/{user_name}"        
            return await self._send_request(url, "post", filtros)       

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
        
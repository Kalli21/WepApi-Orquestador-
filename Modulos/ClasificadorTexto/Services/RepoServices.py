from fastapi import  HTTPException
from typing import List
from .HttpConsult import HttpConsult
from ..CT_request import CT_Sentence, CT_StatsUser

class RepoService(HttpConsult):

    async def subir_comentarios(self, user_id, list_coments: List[CT_Sentence]) :
        
        try:     
            url = f"/subir/{user_id}"   
            return await self._send_request(url, "post", list_coments)       

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
        

    async def get_stats(self, user_id) :
        
        try:     
            url = f"/stats/{user_id}"  
            return await self._send_request(url)       

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
        
    async def update_stats(self, user_id, stats :CT_StatsUser ) :
        
        try:     
            url = f"/stats/{user_id}"  
            return await self._send_request(url,"put", stats)       

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
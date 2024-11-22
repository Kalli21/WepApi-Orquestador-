from fastapi import  HTTPException
from typing import List
from .HttpConsult import HttpConsult

class ModelService(HttpConsult):

    async def determinar_temas_top(self, user_id, num_temas) :
        
        try:     
            url = f"/detTemas/{user_id}/{num_temas}"
            return await self._send_request(url)       

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
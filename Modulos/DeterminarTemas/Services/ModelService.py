from fastapi import  HTTPException
from typing import List
from .HttpConsult import HttpConsult

class ModelService(HttpConsult):

    async def determinar_temas_top(self, user_id, num_temas, predic_all: bool= False) :
        
        try:     
            url = f"/detTemas/{user_id}/{num_temas}"
            if predic_all:
                url += '?predic_all=true'   
            return await self._send_request(url)         

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")        
        
    async def get_cant_temas(self, user_id) :
        
        try:     
            url = f"/canttemas/{user_id}"
            return await self._send_request(url)       

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
        
    async def get_temas(self, user_id, numwords:int) :
        
        try:     
            url = f"/temas/{user_id}/{numwords}"
            return await self._send_request(url)       

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
        

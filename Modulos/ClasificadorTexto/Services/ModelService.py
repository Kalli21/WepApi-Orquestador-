from fastapi import  HTTPException
from typing import List
from .HttpConsult import HttpConsult

class ModelService(HttpConsult):

    async def predecir_sentimiento(self, user_id) :
        
        try:     
            url = "/predecir/" + user_id   
            return await self._send_request(url)       

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
        


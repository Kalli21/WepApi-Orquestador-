
from fastapi import  HTTPException

from .HttpConsult import HttpConsult
from ..PS_response import PS_Response
from ..PS_request import Archivo

class ArchivoService(HttpConsult):

    async def crear_archivo(self, arch: Archivo) -> PS_Response:
        
        try:     
            url = "/Archivo"        
            return await self._send_request(url, "post", arch)       

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
        
    
    async def update_archivo(self, arch: Archivo) -> PS_Response:
        
        try:     
            url = f"/Archivo/{arch.id}"        
            return await self._send_request(url, "put", arch)       

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
        
    async def get_archivo(self, id: int) -> PS_Response:
        
        try:     
            url = f"/Archivo/{id}"        
            return await self._send_request(url)       

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")

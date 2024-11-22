
from fastapi import  HTTPException

from .HttpConsult import HttpConsult
from ..PS_response import PS_Response
from ..PS_request import Usuario

class UsuarioService(HttpConsult):
    
    async def autorizacion_usuario(self) -> PS_Response:        
        try:
            url = "/Usuario/Autorizacion"        
            return await self._send_request(url)   
        
        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
        
    async def get_usuario(self, user_name) -> PS_Response:        
        try:      
            url = f"/Usuario/{user_name}"        
            return await self._send_request(url)   
        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
        
    async def update_usuario(self, user: Usuario) -> PS_Response:        
        try:      
            url = f"/Usuario/{user.userName}"        
            return await self._send_request(url,'put', user)
         
        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
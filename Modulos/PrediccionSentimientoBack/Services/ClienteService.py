
from fastapi import  HTTPException

from .HttpConsult import HttpConsult
from ..PS_response import PS_Response
from ..PS_request import Cliente

class ClienteService(HttpConsult):

    ## CLIENTE
    async def crear_cliente(self, cliente: Cliente) -> PS_Response:
        
        try:     
            url = "/Cliente"        
            return await self._send_request(url, "post", cliente)       

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")

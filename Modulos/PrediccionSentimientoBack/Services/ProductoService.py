
from fastapi import  HTTPException

from .HttpConsult import HttpConsult
from ..PS_response import PS_Response
from ..PS_request import Producto

class ProductoService(HttpConsult):
    
    async def crear_producto(self, producto: Producto) -> PS_Response:        
        try:   
            url = "/Producto"        
            return await self._send_request(url, "post", producto)       

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")

    async def add_categoria(self, idProd: int, idCat: int) -> PS_Response:
        
        try:  
            url = f"/Producto/addCategoria/{idProd}/{idCat}"        
            return await self._send_request(url)       

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
        
    async def get_producto_filtros(self, userName:str , producto: Producto) -> PS_Response:        
        try:   
            url = f"/Producto/username/{userName}"        
            return await self._send_request(url, "post", producto)       

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")

    async def get_producto(self, id: int) -> PS_Response:        
        try:   
            url = f"/Producto/{id}"        
            return await self._send_request(url)       

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
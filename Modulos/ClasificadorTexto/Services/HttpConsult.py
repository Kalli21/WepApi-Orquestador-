from fastapi import  HTTPException
import httpx
from pydantic import BaseModel

from Environments.environments import apiClasModelUrl


class HttpConsult():
           
    def __init__(self, headers):
        self.base_url = apiClasModelUrl
        self.headers = headers
    
    async def _send_request(self, url, tipo = "get", body = None):
        try:
            url = self.base_url + url            
            if isinstance(body, list): 
                body = [item.model_dump(exclude_unset=True) for item in body] 
            elif isinstance(body, BaseModel): 
                body = body.model_dump(exclude_unset=True)
                       
            # Realizar la solicitud HTTP al servicio .NET
            async with httpx.AsyncClient(timeout=1800.0, verify=False) as client:
                if tipo == "get":
                    response = await client.get(url, headers=self.headers)
                if tipo == "post":
                    response = await client.post(url, headers=self.headers, json=body)
                if tipo == "put":
                    response = await client.put(url, headers=self.headers, json=body)
                if tipo == "delete":
                    response = await client.delete(url, headers=self.headers)
            
            # Verificar el código de estado HTTP
            if response.status_code//10 != 20:
                raise HTTPException(
                    status_code=response.status_code,
                    detail= response.json()
                )
            
            # Parsear la respuesta JSON al modelo ResponseDTO
            response_data = response.json()
            return response_data

        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"Error de conexión: {exc}")
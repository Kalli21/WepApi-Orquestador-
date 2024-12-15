from fastapi import  HTTPException
import httpx

from Environments.environments import NET_API_BASE_URL
from ..PS_response import PS_Response

class HttpConsult():
           
    def __init__(self, headers):
        self.base_url = NET_API_BASE_URL
        self.headers = headers
    
    async def _send_request(self, url, tipo = "get", body = None)-> PS_Response:
        try:
            url = self.base_url + url
            if body: body = body.model_dump(exclude_unset=True)   
            # Realizar la solicitud HTTP al servicio .NET
            async with httpx.AsyncClient(verify=False) as client:
                if tipo == "get":
                    response = await client.get(url, headers=self.headers)
                if tipo == "post":
                    if len(body) == 0 : body = {}
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
            return PS_Response(**response_data)

        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"Error de conexión: {exc}")
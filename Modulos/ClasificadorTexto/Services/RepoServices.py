from fastapi import  HTTPException
from typing import List, Optional
from .HttpConsult import HttpConsult
from ..CT_request import CT_Sentence, CT_StatsUser, CT_InfoGrafGeneral
from ProcesarData.PD_request import GeneralInfoFiltro

class RepoService(HttpConsult):

    async def subir_comentarios(self, user_id, list_coments: List[CT_Sentence], persit_stats: Optional[bool] = False ) :
        
        try:     
            url = f"/subir/{user_id}"
            if persit_stats:
                url += '?persit_stats=true'
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
        
    async def get_comentarios(self, user_id, filtros: Optional[GeneralInfoFiltro] = GeneralInfoFiltro()) :
        
        try:     
            url = f"/comentarios/{user_id}"   
            return await self._send_request(url, "post", filtros)       

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
        
    
    ## CREAR INFO
        
    async def create_info_general(self, user_id, info: CT_InfoGrafGeneral ) :
        
        try:     
            url = f"/info/general/{user_id}"   
            return await self._send_request(url, "post", info)       

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
        
    async def create_info_producto(self, user_id, info: CT_InfoGrafGeneral ) :
        
        try:     
            url = f"/info/producto/{user_id}"   
            return await self._send_request(url, "post", info)       

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
        
    async def delete_info_usuario(self, user_id):        
        try:      
            url = f"/delete/{user_id}"        
            return await self._send_request(url,'delete')
         
        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
        
    
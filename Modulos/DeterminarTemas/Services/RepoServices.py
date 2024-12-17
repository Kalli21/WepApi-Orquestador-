
from fastapi import  HTTPException
from typing import List, Optional
from .HttpConsult import HttpConsult
from ..DT_request import DT_Sentence, DT_StatsUser, DT_FiltroSentences, DT_InfoGrafGeneral

class RepoService(HttpConsult):

    async def subir_comentarios(self, user_id,list_coments: List[DT_Sentence], persit_stats: Optional[bool] = False ) :
        
        try:     
            url = "/subir/" + user_id
            if persit_stats:
                url += '?persit_stats=true'
            return await self._send_request(url, "post", list_coments)       

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
        
    async def get_stats(self, user_id) :
        
        try:     
            url = "/stats/" + user_id   
            return await self._send_request(url)       

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
        
    async def update_stats(self, user_id, stats :DT_StatsUser ) :
        
        try:     
            url = "/stats/" + user_id   
            return await self._send_request(url,"put", stats)       

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")


    async def get_sentences(self, user_id, filtro :DT_FiltroSentences ) :
        
        try:     
            url = f"/comentarios/{user_id}"  
            return await self._send_request(url,"post", filtro)       

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
        
    ## CREAR INFO
        
    async def create_info_general(self, user_id, info: DT_InfoGrafGeneral ) :
        
        try:     
            url = f"/info/general/{user_id}"   
            return await self._send_request(url, "post", info)       

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
        
    async def create_info_producto(self, user_id, info: DT_InfoGrafGeneral ) :
        
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
        
    async def get_info_general(self, user_id) :
        
        try:     
            url = f"/info/general/{user_id}"   
            return await self._send_request(url)       

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
        
    async def get_info_producto(self, user_id) :
        
        try:     
            url = f"/info/producto/{user_id}"   
            return await self._send_request(url)       

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
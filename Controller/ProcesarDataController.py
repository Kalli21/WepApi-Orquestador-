from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import JSONResponse
from ProcesarData.procesarData_main import ProcesarData
from Modulos.PrediccionSentimientoBack.PS_request import  Usuario
from Modulos.FirebaseStorage.FS_main import FbConsult
from Modulos.PrediccionSentimientoBack.PS_main import ServiceConsult
from Modulos.ResponseDTO import ResponseDTO

from Modulos.ClasificadorTexto.CT_main import CT_ServiceConsult
from Modulos.DeterminarTemas.DT_main import DT_ServiceConsult
from Modulos.ClasificadorTexto.CT_request import CT_StatsUser
from Modulos.DeterminarTemas.DT_request import DT_StatsUser

import asyncio

app = APIRouter()

@app.post("/ProcesarArchivo/{user_name}")
async def procesar_archivo(request :Request,user_name: str,id_arch: int):
    
    head = request.headers.get('Authorization')
    head = {"Authorization": head}
    consult =  ServiceConsult(head)
    storage = FbConsult()
    aux_user = None
    try:        
        #Autorizacion        
        await consult.usuario_service.autorizacion_usuario()
        # Cambiar esta de usuario a 2
        
        resp_user = await consult.usuario_service.get_usuario(user_name)
        user = Usuario(**resp_user.result)               
        aux_user = user
        # Obetner Datos
        arch = None
        if user.archivos and len(user.archivos)>0:
            for ar in user.archivos:
                if ar.id == id_arch: 
                    arch = ar
                    break
        if not arch:
            resp = ResponseDTO()
            resp.isSuccess = False
            resp.displayMessage = f"El archivo con id {id_arch} no encontrado."
            
            status_code = status.HTTP_404_NOT_FOUND
            
            return JSONResponse(status_code=status_code, content=resp.model_dump())
        
        user.estado = 2        
        await consult.usuario_service.update_usuario(user)
        
        dat = await storage.fb_storage.get_file(arch.url)
        
        # Procesar Datos
        procesar_data = ProcesarData(head,user.id,user.userName)
        resp = await procesar_data.procesar_archivo(dat, arch.separador)
        
        user.estado = 1        
        await consult.usuario_service.update_usuario(user)
        
        return resp    
        

    except ValueError as exc:
        if aux_user:
            aux_user.estado = 1        
            await consult.usuario_service.update_usuario(aux_user)
        raise HTTPException(status_code=500, detail=f"Error al procesar la carga de datos: {exc}")
    except Exception as exc:
        if aux_user:
            aux_user.estado = 1        
            await consult.usuario_service.update_usuario(aux_user)
        raise HTTPException(status_code=500, detail=f"Error inesperado: {exc}")
    

@app.post("/EjecutarAnalisis/{user_name}")
async def ejecutar_analisis(request :Request, user_name: str, num_temas: int):
    
    head = request.headers.get('Authorization')
    head = {"Authorization": head}
    consult =  ServiceConsult(head)

    try:        
        #Autorizacion        
        await consult.usuario_service.autorizacion_usuario()
        
        CT_consult = CT_ServiceConsult(head)
        DT_consult = DT_ServiceConsult(head)
        
        
        # Cambiar Estado Usuario Modelos
        CT_stats = await CT_consult.repo_service.get_stats(user_name)
        CT_stats = CT_StatsUser(**CT_stats)
        CT_stats.estado = 1        
        await CT_consult.repo_service.update_stats(user_name, CT_stats)
        
        DT_stats = await DT_consult.repo_service.get_stats(user_name)
        DT_stats = DT_StatsUser(**DT_stats)
        DT_stats.estado = 1        
        await DT_consult.repo_service.update_stats(user_name, DT_stats)
        
        # Ejecutar Analisis
        await asyncio.gather(
            CT_consult.model_service.predecir_sentimiento(user_name),
            DT_consult.model_service.determinar_temas_top(user_name, num_temas)
        )
        
        # Cambiar Estado Usuario Modelos
        CT_stats = await CT_consult.repo_service.get_stats(user_name)
        CT_stats = CT_StatsUser(**CT_stats)
        CT_stats.estado = 2        
        await CT_consult.repo_service.update_stats(user_name, CT_stats)
        
        DT_stats = await DT_consult.repo_service.get_stats(user_name)
        DT_stats = DT_StatsUser(**DT_stats)
        DT_stats.estado = 2        
        await DT_consult.repo_service.update_stats(user_name, DT_stats)
        
        #Generar Informacion
        
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=f"Error al procesar la carga de datos: {exc}")
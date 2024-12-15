from fastapi import APIRouter, Request, HTTPException, status
from typing import  Optional
from fastapi.responses import JSONResponse
from ProcesarData.ProcesarDataMain import ProcesarDataMain
from ProcesarData.PD_request import GeneralInfoFiltro
from Modulos.PrediccionSentimientoBack.PS_request import  Usuario
from Modulos.FirebaseStorage.FS_main import FbConsult
from Modulos.PrediccionSentimientoBack.PS_main import ServiceConsult
from Modulos.ResponseDTO import ResponseDTO

from Modulos.ClasificadorTexto.CT_main import CT_ServiceConsult
from Modulos.DeterminarTemas.DT_main import DT_ServiceConsult
from Modulos.ClasificadorTexto.CT_request import CT_StatsUser, CT_InfoGrafGeneral
from Modulos.DeterminarTemas.DT_request import DT_StatsUser, DT_InfoGrafGeneral

import asyncio

app = APIRouter()

@app.post("/ProcesarArchivo/{user_name}")
async def procesar_archivo(request :Request,user_name: str,id_arch: int, clean_data_user: Optional[bool] = False):

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

        if user.estado == 2:
            status_code = status.HTTP_226_IM_USED
            return JSONResponse(status_code=status_code, content=f"El usuario {user_name} ya esta procesando un archivo")

        user.estado = 2
        await consult.usuario_service.update_usuario(user)

        # Limpiar Data
        persist_stast = True
        if clean_data_user:
            await consult.usuario_service.delete_info_usuario(user)
            CT_consult = CT_ServiceConsult(head)
            DT_consult = DT_ServiceConsult(head)
            await CT_consult.repo_service.delete_info_usuario(user_name)
            await DT_consult.repo_service.delete_info_usuario(user_name)
            persist_stast = False

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

        dat = await storage.fb_storage.get_file(arch.url)

        # Procesar Datos
        procesar_data = ProcesarDataMain(head,user.id,user.userName,persist_stast)
        resp = await procesar_data.file.procesar_archivo(dat, arch.separador)

        user.estado = 3
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
async def ejecutar_analisis(request :Request, user_name: str, num_temas: int, predic_all: Optional[bool]= False):

    head = request.headers.get('Authorization')
    head = {"Authorization": head}
    consult =  ServiceConsult(head)
    CT_stats = None
    DT_stats = None
    try:
        #Autorizacion
        await consult.usuario_service.autorizacion_usuario()

        resp_user = await consult.usuario_service.get_usuario(user_name)
        user = Usuario(**resp_user.result)
        if user.estado != 3:
            status_code = status.HTTP_404_NOT_FOUND
            return JSONResponse(status_code=status_code, content=f"El usuario {user_name} no ha procesado el archivo.")

        CT_consult = CT_ServiceConsult(head)
        DT_consult = DT_ServiceConsult(head)

        # Cambiar Estado Usuario Modelos -- Inicio Analisis
        CT_stats = await CT_consult.repo_service.get_stats(user_name)
        CT_stats = CT_StatsUser(**CT_stats)

        if CT_stats.estado == 1:
            status_code = status.HTTP_226_IM_USED
            return JSONResponse(status_code=status_code, content=f"El usuario {user_name} tiene un analisis en proceso.")

        CT_stats.estado = 1
        await CT_consult.repo_service.update_stats(user_name, CT_stats)

        DT_stats = await DT_consult.repo_service.get_stats(user_name)
        DT_stats = DT_StatsUser(**DT_stats)
        DT_stats.estado = 1
        await DT_consult.repo_service.update_stats(user_name, DT_stats)

        # Ejecutar Analisis
        await asyncio.gather(
            CT_consult.model_service.predecir_sentimiento(user_name, predic_all),
            DT_consult.model_service.determinar_temas_top(user_name, num_temas, predic_all)
        )

        # Cambiar Estado Usuario Modelos -- Fin Analisis
        CT_stats = await CT_consult.repo_service.get_stats(user_name)
        CT_stats = CT_StatsUser(**CT_stats)
        CT_stats.estado = 2
        await CT_consult.repo_service.update_stats(user_name, CT_stats)

        DT_stats = await DT_consult.repo_service.get_stats(user_name)
        DT_stats = DT_StatsUser(**DT_stats)
        DT_stats.estado = 2
        await DT_consult.repo_service.update_stats(user_name, DT_stats)

        #Generar Informacion
        filtros = GeneralInfoFiltro()
        filtros.PS_filtros_com.userName = user_name
        filtros.cant_ranking = 10
        resp_gen_info = await generar_info(request, user_name, filtros)

        return resp_gen_info
    
    except ValueError as exc:
        if CT_stats:
            CT_stats.estado = 0
            await CT_consult.repo_service.update_stats(user_name, CT_stats)
        if DT_stats:
            DT_stats.estado = 0
            await DT_consult.repo_service.update_stats(user_name, DT_stats)
        raise HTTPException(status_code=500, detail=f"Error al ejecutar el analisis: {exc}")
    except Exception as exc:
        if CT_stats:
            CT_stats.estado = 0
            await CT_consult.repo_service.update_stats(user_name, CT_stats)
        if DT_stats:
            DT_stats.estado = 0
            await DT_consult.repo_service.update_stats(user_name, DT_stats)
        raise HTTPException(status_code=500, detail=f"Error inesperado: {exc}")

@app.post("/GenerarInfo/{user_name}")
async def generar_info(request :Request, user_name: str, filtros: GeneralInfoFiltro):
    head = request.headers.get('Authorization')
    head = {"Authorization": head}
    consult =  ServiceConsult(head)
    CT_stats = None
    DT_stats = None
    try:
        #Autorizacion
        await consult.usuario_service.autorizacion_usuario()

        CT_consult = CT_ServiceConsult(head)
        DT_consult = DT_ServiceConsult(head)

        # Cambiar Estado Usuario Modelos -- Inicio Obtencio de Informacion
        CT_stats = await CT_consult.repo_service.get_stats(user_name)
        CT_stats = CT_StatsUser(**CT_stats)

        if CT_stats.estado == 3:
            status_code = status.HTTP_226_IM_USED
            return JSONResponse(status_code=status_code, content=f"El usuario {user_name} esta generarndo informacion.")

        CT_stats.estado = 3
        await CT_consult.repo_service.update_stats(user_name, CT_stats)

        DT_stats = await DT_consult.repo_service.get_stats(user_name)
        DT_stats = DT_StatsUser(**DT_stats)
        DT_stats.estado = 3
        await DT_consult.repo_service.update_stats(user_name, DT_stats)

        resp_user = await consult.usuario_service.get_usuario(user_name)
        user = Usuario(**resp_user.result)

        # Procesar Datos
        procesar_data = ProcesarDataMain(head,user.id,user.userName,filtros=filtros)

        cal_prod = None

        if filtros.PS_filtros_com.idProducto:
            cal_prod = True
        else:
            cal_prod = False

        resp = await procesar_data.graf.get_comentarios_min_info(calcular=True, cal_prod=cal_prod, cal_temas=True)

        if resp:
            req = CT_InfoGrafGeneral()
            req.graf_circulo = procesar_data.graf.graf_circulo
            req.graf_rank_pos = procesar_data.graf.graf_rankin_top
            req.graf_rank_neg = procesar_data.graf.graf_rankin_neg_top
            req.graf_bar_cat = procesar_data.graf.graf_bar_cat
            req.graf_bar_date = procesar_data.graf.graf_bar_date

            req_dt = DT_InfoGrafGeneral()
            req_dt.graf_word_cloud = procesar_data.graf.graf_word_cloud

            if not cal_prod:
                resp_ct = await CT_consult.repo_service.create_info_general(user_name, req)
                resp_dt = await DT_consult.repo_service.create_info_general(user_name, req_dt)
            else:
                resp_ct = await CT_consult.repo_service.create_info_producto(user_name, req)
                resp_dt = await DT_consult.repo_service.create_info_producto(user_name, req_dt)

        # Cambiar Estado Usuario Modelos -- Fin de Obtencion de Informacion
        CT_stats = await CT_consult.repo_service.get_stats(user_name)
        CT_stats = CT_StatsUser(**CT_stats)
        CT_stats.estado = 4
        await CT_consult.repo_service.update_stats(user_name, CT_stats)

        DT_stats = await DT_consult.repo_service.get_stats(user_name)
        DT_stats = DT_StatsUser(**DT_stats)
        DT_stats.estado = 4
        await DT_consult.repo_service.update_stats(user_name, DT_stats)

        return f"{resp_ct} en CT y {resp_dt} en DT"

    except ValueError as exc:
        if CT_stats:
            CT_stats.estado = 2
            await CT_consult.repo_service.update_stats(user_name, CT_stats)
        if DT_stats:
            DT_stats.estado = 2
            await DT_consult.repo_service.update_stats(user_name, DT_stats)
        raise HTTPException(status_code=500, detail=f"Error al ejecutar el analisis: {exc}")
    except Exception as exc:
        if CT_stats:
            CT_stats.estado = 2
            await CT_consult.repo_service.update_stats(user_name, CT_stats)
        if DT_stats:
            DT_stats.estado = 2
            await DT_consult.repo_service.update_stats(user_name, DT_stats)
        raise HTTPException(status_code=500, detail=f"Error inesperado: {exc}")
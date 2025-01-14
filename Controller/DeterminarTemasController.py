from fastapi import APIRouter, Request, HTTPException
from Modulos.DeterminarTemas.DT_main import DT_ServiceConsult
from Modulos.PrediccionSentimientoBack.PS_main import ServiceConsult

app = APIRouter()

@app.get("/temas/{userName}/{numWord}")
async def get_autorizacion(request :Request, userName: str, numWord: int):
    try:
        head = request.headers.get('Authorization')
        head = {"Authorization": head}
        consult =  ServiceConsult(head)
        #Autorizacion
        await consult.usuario_service.autorizacion_usuario()
        
        dt_consult =  DT_ServiceConsult(head)
        resp = await dt_consult.repo_service.get_temas(userName, numWord)
        return resp
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=f"Error en el Login: {exc}")
     

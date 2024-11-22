from fastapi import APIRouter, Request
from Modulos.PrediccionSentimientoBack.PS_main import ServiceConsult


app = APIRouter()

@app.get("/usuario/autorizacion")
async def get_autorizacion(request :Request):
    consult =  ServiceConsult(request.headers)
    resp = await consult.usuario_service.autorizacion_usuario()
    return resp


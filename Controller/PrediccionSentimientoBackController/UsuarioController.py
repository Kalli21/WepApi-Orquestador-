from fastapi import APIRouter, Request, HTTPException
from Modulos.PrediccionSentimientoBack.PS_main import ServiceConsult
from Modulos.PrediccionSentimientoBack.PS_request import Usuario

app = APIRouter()

@app.get("/Usuario/Autorizacion")
async def get_autorizacion(request :Request):
    try:
        consult =  ServiceConsult(request.headers)
        resp = await consult.usuario_service.autorizacion_usuario()
        return resp
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=f"Usuario no autorizado: {exc}")
# -----------------------------------------------------------
@app.post("/Usuario/Login")
async def get_autorizacion(request :Request, user: Usuario):
    try:
        consult =  ServiceConsult(None)
        resp = await consult.usuario_service.login_usuario(user)
        return resp
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=f"Error en el Login: {exc}")
     
@app.post("/Usuario/Register")
async def get_autorizacion(request :Request, user: Usuario):
    try:
        consult =  ServiceConsult(None)
        resp = await consult.usuario_service.register_usuario(user)
        return resp
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=f"Error al Registrar: {exc}")
    
@app.get("/Usuario")
async def get_all_usuarios(request :Request):
    try:
        head = request.headers.get('Authorization')
        head = {"Authorization": head}
        consult =  ServiceConsult(head)
        resp = await consult.usuario_service.get_all_usuario()
        return resp
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=f"Error al obtener usuarios: {exc}")

@app.get("/Usuario/{id}")
async def get_usuario_by_id(request :Request, userName: str):
    try:
        head = request.headers.get('Authorization')
        head = {"Authorization": head}
        consult =  ServiceConsult(head)
        resp = await consult.usuario_service.get_usuario(userName)
        return resp
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=f"Error al obtener usuario: {exc}")

  
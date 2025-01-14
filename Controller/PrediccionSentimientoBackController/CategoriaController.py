from fastapi import APIRouter, Request, HTTPException
from Modulos.PrediccionSentimientoBack.PS_main import ServiceConsult

app = APIRouter()

@app.get("/Categoria/username/{userName}")
async def get_autorizacion(request :Request, userName: str):
    try:
        head = request.headers.get('Authorization')
        head = {"Authorization": head}
        consult =  ServiceConsult(head)
        resp = await consult.categoria_service.get_categoria_by_user(userName)
        return resp
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=f"Error: {exc}")
     

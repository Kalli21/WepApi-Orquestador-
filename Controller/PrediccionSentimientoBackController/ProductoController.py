from fastapi import APIRouter, Request, HTTPException
from Modulos.PrediccionSentimientoBack.PS_main import ServiceConsult
from Modulos.PrediccionSentimientoBack.PS_request import PS_ProductoFiltros

app = APIRouter()

@app.post("/Producto/username/{userid}")
async def get_autorizacion(request :Request, userid: str, filtros:PS_ProductoFiltros ):
    try:
        head = request.headers.get('Authorization')
        head = {"Authorization": head}
        consult =  ServiceConsult(head)
        resp = await consult.producto_service.get_producto_filtros(userid, filtros)
        return resp
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=f"Error: {exc}")
    
@app.get("/Producto/{id}")
async def get_autorizacion(request :Request, id: int ):
    try:
        head = request.headers.get('Authorization')
        head = {"Authorization": head}
        consult =  ServiceConsult(head)
        resp = await consult.producto_service.get_producto(id)
        return resp
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=f"Error: {exc}")
     

from fastapi import APIRouter, File, UploadFile, Request, HTTPException, status
from fastapi.responses import JSONResponse
from Modulos.PrediccionSentimientoBack.PS_request import Archivo, Usuario
from Modulos.FirebaseStorage.FS_main import FbConsult
from Modulos.PrediccionSentimientoBack.PS_main import ServiceConsult


app = APIRouter()

@app.post("/upload/{user_name}")
async def upload_file(request :Request,user_name: str,sep: str, file: UploadFile = File(...)):
    try:
        head = request.headers.get('Authorization')
        head = {"Authorization": head}
        consult =  ServiceConsult(head)
        storage = FbConsult()
                
        #Autorizacion        
        await consult.usuario_service.autorizacion_usuario()
                
        arch_resp = await storage.fb_storage.upload_file(file)    
        
        resp_user = await consult.usuario_service.get_usuario(user_name)
        user = Usuario(**resp_user.result)  
        
        ## solo se mantiene 1 archivo
        if user.archivos and len(user.archivos)>0:
            
            arch = user.archivos[0]
            # Eliminar anterior
            await storage.fb_storage.eliminar_archivo_firebase(arch.url)            
            
            arch.nombre = file.filename
            arch.separador = sep
            arch.url = arch_resp['url']
            
            resp = await consult.archivo_service.update_archivo(arch)
            
            status_code = status.HTTP_200_OK
        else:
        
            #Guardar Archivo
            arch = Archivo()
            arch.nombre = file.filename
            arch.separador = sep
            arch.url = arch_resp['url']
            arch.usuarioId = user.id

            status_code = status.HTTP_201_CREATED
            
            resp = await consult.archivo_service.crear_archivo(arch)
        
        return JSONResponse(status_code=status_code, content=resp.model_dump())

    except ValueError as exc:
        raise HTTPException(status_code=500, detail=f"Error al procesar la carga de datos: {exc}")
    

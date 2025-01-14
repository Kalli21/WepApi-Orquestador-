from fastapi import APIRouter
from .PrediccionSentimientoBackController.PrediccionSentimientoBackController import app as PS_app
from .FirebaseStorageController import app as FS_app
from .ProcesarDataController import app as PD_app
from .DeterminarTemasController import app as DT_app

app = APIRouter()

# Incluye las rutas y configuraciones de la base de datos de sql_app en la aplicación principal
app.include_router(PS_app)
app.include_router(FS_app)
app.include_router(PD_app)
app.include_router(DT_app)
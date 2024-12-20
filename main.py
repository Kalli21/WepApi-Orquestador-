from fastapi import FastAPI
from Controller.main_controller import app as app_controller
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# Configuración de CORS
origins = [
    "http://localhost",
    "http://localhost:4200",
    "http://127.0.0.1:8888",
    "http://54.87.222.35",
    "http://54.83.42.195:8080",
    "http://proyecto-tesis-acfront-angular.s3-website-us-east-1.amazonaws.com"    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluye las rutas y configuraciones de la base de datos de sql_app en la aplicación principal
app.include_router(app_controller)
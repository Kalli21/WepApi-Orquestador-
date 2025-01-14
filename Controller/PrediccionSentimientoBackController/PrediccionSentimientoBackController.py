from fastapi import APIRouter
from .UsuarioController import app as user_app
from .ProductoController import app as prod_app
from .CategoriaController import app as cat_app

app = APIRouter()

app.include_router(user_app)
app.include_router(prod_app)
app.include_router(cat_app)

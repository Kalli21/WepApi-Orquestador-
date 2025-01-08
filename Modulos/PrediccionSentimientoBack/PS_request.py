from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Comentario(BaseModel):
    id: int = None
    contenido: str = None
    fecha: str = None
    estado: int = None
    productoId: int = None
    clienteId: int = None
    userName: str = None
    
class Categoria(BaseModel):
    id: int = None
    nombre: str = None
    userName: str = None
    
class Producto(BaseModel):
    id: int = None
    codProducto: str = None
    nombre: str = None
    descripcion: str = None
    precio: float = None
    urlImg: str = None
    usuarioId: int = None
    categorias: List[Categoria] = None
    comentarios: List[Comentario] = None

class Cliente(BaseModel):
    id: int = None
    nombre: Optional[str] = None
    codCliente: str = None
    comentarios: Optional[List[Comentario]] = None
    userName: str = None

class Comentario(BaseModel):
    id: int = None
    contenido: Optional[str] = None
    fecha: Optional[str] = None
    estado: int = None
    productoId: int = None
    clienteId: int = None
    userName: Optional[str] = None
    
class Archivo(BaseModel):
    id: Optional[int] = None
    nombre: Optional[str] = None
    separador: str = None
    finLinea: Optional[str] = None
    url: str = None
    usuarioId: int = None


class Usuario(BaseModel):
    id: int = None
    userName: str = None
    nombres: Optional[str] = None
    correo: Optional[str] = None
    password: Optional[str] = None
    token: Optional[str] = None
    activo: bool = None
    estado: int = None
    productos: Optional[List[Producto]] = None
    archivos: Optional[List[Archivo]] = None
    
### FILTROS

class PS_CategoriasFiltros(BaseModel):
    fechaIni: Optional[str] = None
    fechaFin: Optional[str] = None
    categoriasId: List[int] = []

class PS_ComentariosFiltros(BaseModel):
    pageNumber: Optional[int] = 1
    pageSize: Optional[int] = 10
    totalPages: Optional[int] = None
    totalItems: Optional[int] = None
    paginacion: Optional[bool] = False
    fechaIni: Optional[str] = None 
    fechaFin: Optional[str] = None
    idProducto: Optional[int] = None
    categoriasId: Optional[List[int]] = None
    userName: Optional[str] = None 
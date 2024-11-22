
from .Services.CategoriaService import CategoriaService 
from .Services.ClienteService import ClienteService 
from .Services.ComentarioService import ComentarioService 
from .Services.UsuarioService import UsuarioService 
from .Services.ProductoService import ProductoService 
from .Services.ArchivoService import ArchivoService 


class ServiceConsult():
    
    def __init__(self, headers):
        self.categoria_service : CategoriaService = CategoriaService(headers)
        self.cliente_service : ClienteService = ClienteService(headers)
        self.comentario_service : ComentarioService = ComentarioService(headers)
        self.usuario_service : UsuarioService = UsuarioService(headers)
        self.producto_service : ProductoService = ProductoService(headers)
        self.archivo_service : ArchivoService = ArchivoService(headers)
        
        
        
         
        
        
        
        
        
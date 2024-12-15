from Modulos.PrediccionSentimientoBack.PS_request import Producto, Categoria, Cliente, Comentario
from Modulos.PrediccionSentimientoBack.PS_main import ServiceConsult
from Modulos.ClasificadorTexto.CT_request import CT_Sentence
from Modulos.ClasificadorTexto.CT_main import CT_ServiceConsult
from Modulos.DeterminarTemas.DT_request import DT_Sentence
from Modulos.DeterminarTemas.DT_main import DT_ServiceConsult

from fastapi import  HTTPException
import pandas as pd
import httpx

class ProcesarFile:    

    HEADER_CSV = ["CodProducto","NombreProducto","DescripcionProducto","PrecioProducto","Imagen", #Info Producto
                  "NombreCategoria", #Info Categoria
                  "CodCliente","NombreCliente", #Info Cliente
                  "Comentario","Fecha"] # Info Comentario
    
       
    def __init__(self, headers, id_user, user_name, persist_stast = False):
        self._PS = ServiceConsult(headers)
        self._CT = CT_ServiceConsult(headers)
        self._DT = DT_ServiceConsult(headers)
        self.id_user = id_user
        self.user_name = user_name
        
        self.msg = ""
        self.productos = []
        self.categorias = []
        self.clientes = []
        self.comentarios = []
        
        self.persist_stast = persist_stast
    
    async def procesar_archivo(self, file, sep = ";"):
        try:    
            self.df = pd.read_csv(file, sep = sep)
                
            if not self._validar_df():
                return self.msg
            self._limpiar_df()
            await self._insertar_productos()
            await self._insertar_categorias()
            await self._insertar_clientes()
            await self._insertar_comentarios()
            await self._match_categoria_producto()
            self.msg = "Archivo Procesado"
            return self.msg
        
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=f"Error de conexión: {exc}")
        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
        
    def _validar_df(self):
        val = True                
        # Convertimos las listas en conjuntos y las comparamos
        val = set(self.HEADER_CSV) == set(self.df.columns.tolist())
        if not val:
            self.msg += f"No se encontro las columas{set(self.HEADER_CSV) - set(self.df.columns.tolist())}\n"        
        return val
    
    def _limpiar_df(self):
        self.df.dropna(axis=0, how='all', inplace= True)
        self.df.dropna(axis=1, how='all', inplace= True)        
        self.df.dropna(subset=['Comentario'], axis=0, inplace= True)
        self.df.drop_duplicates(keep='first', inplace= True)
        
        self.df["CodProducto"] = self.df["CodProducto"].astype(str)
        
        # list_str = set(self.HEADER_CSV) -set('Fecha','PrecioProducto')
        # list_str = list_str.tolist()
        
        # self.df[list_str] = self.df[list_str].astype(str) 
        # self.df['Fecha'] = pd.to_datetime(self.df['Fecha'], format='%d/%m/%Y')       
        # self.df['PrecioProducto'] = self.df['PrecioProducto'].astype(float)   
        
        
    async def _insertar_productos(self):
        self.df_productos = self.df[["CodProducto","NombreProducto","DescripcionProducto","PrecioProducto","Imagen"]].copy()
        # Eliminar filas con valores repetidos en la columna 'A'
        self.df_productos.dropna(subset=['CodProducto'], axis=0, inplace= True)
        self.df_productos.drop_duplicates(subset=['CodProducto'], keep='first', inplace= True)
        
        self.df_productos["IdProducto"] = None
        
        # Iterar usando itertuples
        for row in self.df_productos.itertuples(index=True, name="Row"):
            prod = Producto()
            prod.codProducto = row.CodProducto.strip()
            prod.nombre = row.NombreProducto.strip()
            prod.descripcion = row.DescripcionProducto.strip()
            prod.precio = row.PrecioProducto
            prod.urlImg = row.Imagen
            prod.usuarioId = self.id_user
            
            resp = await self._PS.producto_service.crear_producto(prod)
            
            if resp.isSuccess:
                prod.id = resp.result["id"]
                self.productos.append(prod)
                self.df_productos.loc[row.Index, "IdProducto"] = prod.id

    async def _insertar_categorias(self):
        self.df_categorias = self.df[["NombreCategoria"]].copy()
        # Eliminar filas con valores repetidos en la columna 'A'
        self.df_categorias.dropna(axis=0, inplace= True)
        self.df_categorias.drop_duplicates(keep='first', inplace= True)
        
        self.df_categorias["IdCategoria"] = None
        
        # Iterar usando itertuples
        for row in self.df_categorias.itertuples(index=True, name="Row"):
            cat = Categoria()
            cat.nombre = row.NombreCategoria.strip()
            cat.userName = self.user_name              
            resp = await self._PS.categoria_service.crear_categoria(cat)
            
            if resp.isSuccess:
                cat.id = resp.result["id"]
                self.categorias.append(cat)
                self.df_categorias.loc[row.Index, "IdCategoria"] = cat.id
                
    async def _insertar_clientes(self):
        self.df_clientes = self.df[["CodCliente","NombreCliente"]].copy()
        # Eliminar filas con valores repetidos en la columna 'A'
        self.df_clientes.dropna(subset=['CodCliente'], axis=0, inplace= True)
        self.df_clientes.drop_duplicates(subset=['CodCliente'], keep='first', inplace= True)
        
        self.df_clientes["IdCliente"] = None
        
        # Iterar usando itertuples
        for row in self.df_clientes.itertuples(index=True, name="Row"):
            cli = Cliente()
            cli.nombre = row.NombreCliente.strip()
            cli.codCliente = row.CodCliente.strip()
            cli.userName = self.user_name 
                         
            resp = await self._PS.cliente_service.crear_cliente(cli)
            
            if resp.isSuccess:
                cli.id = resp.result["id"]
                self.clientes.append(cli)
                self.df_clientes.loc[row.Index, "IdCliente"] = cli.id
                
    async def _insertar_comentarios(self):
        df_comentarios = self.df[["CodProducto", "CodCliente","Comentario","Fecha"]]\
            .merge(self.df_productos[["CodProducto","IdProducto"]], how='left', on='CodProducto')\
            .merge(self.df_clientes[["CodCliente","IdCliente"]], how='left', on='CodCliente')
        
        list_com_ct = []
        list_com_dt = []
           
        # Iterar usando itertuples
        for row in df_comentarios.itertuples(index=True, name="Row"):
            com = Comentario()
            com.contenido = row.Comentario.strip()
            if not pd.isna(row.Fecha): com.fecha = pd.to_datetime(row.Fecha.strip(), format='%d/%m/%Y').isoformat()
            com.estado = 1
            com.productoId = row.IdProducto
            com.clienteId = row.IdCliente
            com.userName = self.user_name
                         
            resp = await self._PS.comentario_service.crear_comentario(com)
            
            if resp.isSuccess:
                com.id = resp.result["id"]
                self.comentarios.append(com)
                
                com_ct = CT_Sentence()
                com_ct.id = str(com.id)
                com_ct.text = com.contenido
                com_ct.fecha = com.fecha
                
                com_dt = DT_Sentence()
                com_dt.id = str(com.id)
                com_dt.text = com.contenido 
                com_dt.fecha = com.fecha 
                
                list_com_ct.append(com_ct)
                list_com_dt.append(com_dt)
        
        if len(list_com_ct)>0: await self._CT.repo_service.subir_comentarios(self.user_name, list_com_ct, self.persist_stast)
        if len(list_com_dt)>0: await self._DT.repo_service.subir_comentarios(self.user_name, list_com_dt, self.persist_stast)
        
                
    async def _match_categoria_producto(self):
        match = self.df[["CodProducto","NombreCategoria"]]\
            .merge(self.df_productos[["CodProducto","IdProducto"]], how='left', on='CodProducto')\
            .merge(self.df_categorias[["NombreCategoria","IdCategoria"]], how='left', on='NombreCategoria')
            
        match = match[["IdProducto","IdCategoria"]]
        match.drop_duplicates(keep='first', inplace= True)     
        # Iterar usando itertuples
        for row in match.itertuples(index=True, name="Row"):
            resp = await self._PS.producto_service.add_categoria(row.IdProducto, row.IdCategoria)
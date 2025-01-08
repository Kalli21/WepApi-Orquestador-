import pandas as pd
from fastapi import  HTTPException

from Modulos.PrediccionSentimientoBack.PS_main import ServiceConsult
from Modulos.ClasificadorTexto.CT_response import RelacionComCat
from Modulos.ClasificadorTexto.CT_request import CT_InfoGraf
from Modulos.ClasificadorTexto.CT_main import CT_ServiceConsult
from Modulos.DeterminarTemas.DT_main import DT_ServiceConsult
from Modulos.ComentarioDTO import ComentarioDTO
from .PD_request import GeneralInfoFiltro


class ProcesarDataGraf:
    
    def __init__(self, headers, id_user, user_name, filtros: GeneralInfoFiltro):
        self._PS = ServiceConsult(headers)
        self._CT = CT_ServiceConsult(headers)
        self._DT = DT_ServiceConsult(headers)
        self.id_user = id_user
        self.user_name = user_name
        
        self.CT_filtro_com = filtros.CT_filtro_com
        self.PS_filtros_com = filtros.PS_filtros_com
        self.DT_filtros_com = filtros.DT_filtros_com
        self.msg = ""
        self.com_min_info = []
        
        # Informacion Graficos
        self.graf_circulo = CT_InfoGraf()
        self.graf_rankin_top = []
        self.graf_rankin_neg_top = []
        self.cant_ranking = filtros.cant_ranking
        
        self.graf_bar_cat = []
        self.graf_bar_date = []
        self.graf_word_cloud = []
        
        self.info_comentarios = []
        self.get_coment = filtros.get_comentarios
        self.info_filtro = None
        
    async def get_comentarios_min_info(self, calcular = False, cal_prod = True, cal_temas = False):
        #Obter Comentarios con el filtrado
        
        try:
            resp_cat = await self._PS.comentario_service.get_comentarios_min_info(self.PS_filtros_com)
            
            # if self.get_coment:
            #     aux_info = resp_cat.result
            #     if len(aux_info)>0 :
            #         aux_info = pd.DataFrame(aux_info)
            #         list_ids = aux_info['idComentario'].astype(str).unique().tolist()
            #         self.DT_filtros_com.listId = list_ids
            #         self.CT_filtro_com.listId = list_ids

            data_temas = None
            if cal_temas:
                self.DT_filtros_com.min_info = True
                data_temas = await self._DT.repo_service.get_sentences(self.user_name, self.DT_filtros_com)
                 
            comentarios = await self._CT.repo_service.get_comentarios(self.user_name, self.CT_filtro_com)
                        
            categorias = None
            
            if resp_cat.isSuccess:
                categorias = resp_cat.result
                self.info_filtro = resp_cat.filtroInfo
                if len(categorias)>0 and len(comentarios)>0:
                    
                    # Convertir listas a DataFrames
                    df_categorias = pd.DataFrame(categorias)
                    df_comentarios = pd.DataFrame(comentarios)
                    if cal_temas: 
                        df_temas = pd.DataFrame(data_temas)
                        df_temas = df_temas[['id','tema']]
                        df_temas['id'] = df_temas['id'].astype(str)
                        df_temas.rename(columns={'id': 'id_tema'}, inplace=True)

                    # Asegurar que las claves tengan el mismo tipo
                    df_categorias['idComentario'] = df_categorias['idComentario'].astype(str)
                    df_comentarios['id'] = df_comentarios['id'].astype(str)

                    # Realizar el Left Join
                    df_merge = pd.merge(df_categorias, df_comentarios, left_on='idComentario', right_on='id', how='inner')
                    if cal_temas:
                        df_merge = pd.merge(df_merge, df_temas, left_on='idComentario', right_on='id_tema', how='inner')
                        
                    if calcular: 
                        self._calcular_valores_graf_circulo(df_merge)
                        if not cal_prod: self._calcular_valores_graf_ranking_prod(df_merge)
                        self._calcular_valores_graf_bar_cat(df_merge)
                        self._calcular_valores_graf_bar_date(df_merge)
                        await self._calcular_valores_temas(df_temas, cal_temas)
                        
                    
                    for index, row in df_merge.iterrows():
                        info = RelacionComCat.model_validate(row.to_dict())
                        info.correlativo = index + 1  # Agregar el índice como atributo adicional
                        self.com_min_info.append(info)
                    
                    if self.get_coment:
                        self._obetener_comentarios(df_merge, cal_temas)
                    
                    return True         
                        
            return False

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
        
        
    def _calcular_valores_graf_circulo(self, df):
        #Obter Comentarios con el filtrado
        
        try:     
                        
            # Agrupar por 'categoria' y contar ocurrencias
            df_agrupado = df.groupby(['categoria']).size().reset_index(name='conteo')

            # Crear un pivot con columnas separadas por cada categoría
            df_pivot = df_agrupado.pivot_table(
                index=None,             # Sin índice, se convierte en una tabla plana
                columns='categoria',    # Cada categoría será una columna
                values='conteo',        # Los valores serán los conteos
                fill_value=0            # Rellenar valores faltantes con 0
            ).reset_index(drop=True)
            
            # Verificar y asignar valores solo si existen las columnas
            if 0 in df_pivot.columns: self.graf_circulo.neg = int(df_pivot[0].iloc[0]) 
            if 1 in df_pivot.columns: self.graf_circulo.net = int(df_pivot[1].iloc[0]) 
            if 2 in df_pivot.columns: self.graf_circulo.pos = int(df_pivot[2].iloc[0])  
            self.graf_circulo.total = self.graf_circulo.neg + self.graf_circulo.net + self.graf_circulo.pos

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
        
    def _calcular_valores_graf_ranking_prod(self, df):
        #Obter Comentarios con el filtrado
        
        try:                 
            # Agrupar por 'nombreProducto', 'categoria' y contar ocurrencias
            df_agrupado = df.groupby(['nombreProducto', 'categoria']).size().reset_index(name='conteo')

            # Crear columnas separadas por cada categoría
            df_pivot = df_agrupado.pivot_table(
                index='nombreProducto', 
                columns='categoria', 
                values='conteo', 
                fill_value=0
            ).reset_index()

            if 0 not in df_pivot.columns: df_pivot[0] = 0 
            if 1 not in df_pivot.columns: df_pivot[1] = 0  
            if 2 not in df_pivot.columns: df_pivot[2] = 0 
            
            # Ordenar por las columnas '2', '1' y '0' en ese orden
            df_pivot_sorted = df_pivot.sort_values(by=[2, 1, 0], ascending=[False, False, False])

            for index, row in df_pivot_sorted.head(self.cant_ranking).iterrows():                        
                info = CT_InfoGraf()
                info.correlativo = index + 1 
                info.nombre = row['nombreProducto']
                info.neg = int(row[0])
                info.net = int(row[1])
                info.pos = int(row[2])
                info.total = info.neg + info.net + info.pos
                
                self.graf_rankin_top.append(info)
            
            for index, row in df_pivot_sorted.tail(self.cant_ranking).iterrows():                        
                info = CT_InfoGraf()
                info.correlativo = index + 1
                info.nombre = row['nombreProducto']
                info.neg = int(row[0])
                info.net = int(row[1])
                info.pos = int(row[2])
                info.total = info.neg + info.net + info.pos
                
                self.graf_rankin_neg_top.append(info)
            
        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
        
    def _calcular_valores_graf_bar_cat(self, df):
        #Obter Comentarios con el filtrado
        
        try:                             
            # Agrupar por 'idCategoria' y 'categoria', y conservar el nombreCategoria único
            df_agrupado = df.groupby(['idCategoria', 'categoria']).agg(
                conteo=('idCategoria', 'size'),
                primer_categoria=('nombreCategoria', 'first')
            ).reset_index()

            # Aplicar pivot para convertir las categorías en columnas
            df_pivot = df_agrupado.pivot_table(
                index=['idCategoria', 'primer_categoria'],  # Mantener 'idCategoria' y 'nombreCategoria' como índices
                columns='categoria',                       # Convertir las categorías en columnas
                values='conteo',                           # Los valores serán el conteo
                fill_value=0                               # Llenar valores faltantes con 0
            ).reset_index()

            
            if 0 not in df_pivot.columns: df_pivot[0] = 0 
            if 1 not in df_pivot.columns: df_pivot[1] = 0  
            if 2 not in df_pivot.columns: df_pivot[2] = 0 
            
            for index, row in df_pivot.iterrows():                        
                info = CT_InfoGraf()
                info.correlativo = index
                info.nombre = row['primer_categoria']
                info.neg = int(row[0])
                info.net = int(row[1])
                info.pos = int(row[2])
                info.total = info.neg + info.net + info.pos
                
                self.graf_bar_cat.append(info)
            

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
        
    def _calcular_valores_graf_bar_date(self, df):
        #Obter Comentarios con el filtrado
        
        try:                             
            # Agrupar por 'nombreProducto', 'categoria' y contar ocurrencias
            df_agrupado = df.groupby(['codMes', 'categoria']).size().reset_index(name='conteo')

            # Crear columnas separadas por cada categoría
            df_pivot = df_agrupado.pivot_table(
                index='codMes', 
                columns='categoria', 
                values='conteo', 
                fill_value=0
            ).reset_index()
            
            if 0 not in df_pivot.columns: df_pivot[0] = 0 
            if 1 not in df_pivot.columns: df_pivot[1] = 0  
            if 2 not in df_pivot.columns: df_pivot[2] = 0 
            
            for index, row in df_pivot.iterrows():                        
                info = CT_InfoGraf()
                info.correlativo = index
                info.nombre = row['codMes']
                info.neg = int(row[0])
                info.net = int(row[1])
                info.pos = int(row[2])
                info.total = info.neg + info.net + info.pos
                
                self.graf_bar_date.append(info)
            

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
        
    async def _calcular_valores_temas(self, df, cal_temas):
               
        try:                  
            
            # Agrupar por 'nombreProducto', 'categoria' y contar ocurrencias
            if cal_temas: valores_unicos = df['tema'].unique()

            numwords = await self._DT.model_service.get_cant_temas(self.user_name)
            
            resp_temas = await self._DT.model_service.get_temas(self.user_name,numwords)
            
            for clave, valor in resp_temas.items():
                if cal_temas:
                    if int(clave) in valores_unicos:
                        self.graf_word_cloud.append(valor)
                else:
                    self.graf_word_cloud.append(valor)

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
        
    def _obetener_comentarios(self, df, cal_temas):
        try:            
            for index, row in df.iterrows():
                coment = ComentarioDTO()
                coment.id = int(row['idComentario'])
                coment.correlativo = index + 1
                coment.contenido = row['text']
                coment.fecha = row['fecha']
                coment.producto = row['nombreProducto']
                coment.cliente = row['codCliente']
                
                if cal_temas:
                    coment.tema = row['tema']
                
                coment.sentimiento = str(row['categoria'])
                coment.probabilidad = row['probabilidades']
                
                self.info_comentarios.append(coment)
                

        except ValueError as exc:
            raise HTTPException(status_code=500, detail=f"Error al procesar la respuesta: {exc}")
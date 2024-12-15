from pydantic import BaseModel
from typing import List, Optional

class CT_Sentence(BaseModel):
    id: str = ''
    text: str = None
    probabilidades: List[float] = [] 
    categoria: int = -1
    fecha: str = ''


class CT_StatsBase(BaseModel):
    total: int = 0
    pos: int = 0
    net: int = 0
    neg: int = 0
    
class CT_StatsUser(CT_StatsBase):
    # 0 -> No Analizado ,  1 -> Analisando 2 -> Analisis terminado(generado info) 3 -> Informacion obtenida  
    estado: int = 0

#INFORMACION GRAFICOS

class CT_InfoGraf(CT_StatsBase):
    correlativo: int = 0
    nombre: str = ''


#Filtros
class CT_ComentariosFiltros(BaseModel):
    fechaIni: Optional[str] = None
    fechaFin: Optional[str] = None
    categoriasId: List[int] = [] 
    listId: List[str] = [] 
    

class CT_InfoGrafGeneral(BaseModel):
    graf_circulo: Optional[CT_StatsBase] = None
    graf_rank_pos: Optional[List[CT_InfoGraf]] = None
    graf_rank_neg: Optional[List[CT_InfoGraf]] = None
    graf_bar_cat: Optional[List[CT_InfoGraf]] = None
    graf_bar_date: Optional[List[CT_InfoGraf]] = None
  
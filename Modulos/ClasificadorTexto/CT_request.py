from pydantic import BaseModel
from typing import List, Optional

class CT_Sentence(BaseModel):
    id: str = ''
    text: str = None
    probabilidades: List[float] = [] 
    categoria: int = -1
    fecha: str = ''


class CT_StatsUser(BaseModel):
    total: int = 0
    pos: int = 0
    net: int = 0
    neg: int = 0
    # 0 -> No Analizado ,  1 -> Analisando 2 -> Analisis terminado(generado info) 3 -> Informacion obtenida  
    estado: int = 0
    
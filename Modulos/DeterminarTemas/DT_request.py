from pydantic import BaseModel
from typing import List, Optional

class DT_Sentence(BaseModel):
    id: str = ''
    text: str = None
    temas: dict = {} 
    fecha: str = ''
    
class DT_StatsUser(BaseModel):
    total: int = 0
    # 0 -> No Analizado ,  1 -> Analisando 2 -> Analisis terminado(generado info) 3 -> Informacion obtenida  
    estado: int = 0
    
class DT_FiltroSentences(BaseModel):
    fechaIni: Optional[str] = None
    fechaFin: Optional[str] = None
    temasId: List[int] = []
    listId: List[str] = []  
    min_info : Optional[bool] = False
    
#######
class DT_InfoGrafGeneral(BaseModel):
    graf_word_cloud: Optional[List[dict]] = None
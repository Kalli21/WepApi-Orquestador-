from pydantic import BaseModel

class DT_Sentence(BaseModel):
    id: str = ''
    text: str = None
    temas: dict = {} 
    fecha: str = ''
    
class DT_StatsUser(BaseModel):
    total: int = 0
    # 0 -> No Analizado ,  1 -> Analisando 2 -> Analisis terminado(generado info) 3 -> Informacion obtenida  
    estado: int = 0
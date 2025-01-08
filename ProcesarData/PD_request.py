from pydantic import BaseModel
from typing import List, Optional

from Modulos.PrediccionSentimientoBack.PS_request import PS_ComentariosFiltros
from Modulos.ClasificadorTexto.CT_request import CT_ComentariosFiltros
from Modulos.DeterminarTemas.DT_request import DT_FiltroSentences

class GeneralInfoFiltro(BaseModel):
    CT_filtro_com: Optional[CT_ComentariosFiltros] = CT_ComentariosFiltros()
    PS_filtros_com: Optional[PS_ComentariosFiltros] = PS_ComentariosFiltros()
    DT_filtros_com: Optional[DT_FiltroSentences] = DT_FiltroSentences()
    cant_ranking: Optional[int] = None
    get_comentarios: Optional[bool] = False
    
  
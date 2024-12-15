
from .ProcesarFile import ProcesarFile
from .ProcesarDataGraf import ProcesarDataGraf
from .PD_request import GeneralInfoFiltro

class ProcesarDataMain:
    
    def __init__(self,headers, id_user, user_name, persist_stast = False, filtros:GeneralInfoFiltro = GeneralInfoFiltro()):
        self.file = ProcesarFile(headers, id_user, user_name, persist_stast)
        self.graf = ProcesarDataGraf(headers, id_user, user_name, filtros)
        
   
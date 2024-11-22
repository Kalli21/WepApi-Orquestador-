
from .Services.RepoServices import RepoService
from .Services.ModelService import ModelService


class DT_ServiceConsult():
    
    def __init__(self, headers):
        self.repo_service   : RepoService    = RepoService(headers)
        self.model_service  : ModelService  = ModelService(headers)
        
        
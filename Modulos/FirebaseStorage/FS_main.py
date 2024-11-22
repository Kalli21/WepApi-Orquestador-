
from firebase_admin import credentials, initialize_app

from .Services.FbSotorageService import FbStorageService
# Inicializar la app de Firebase
cred = credentials.Certificate("Credenciales\\angular-html-57b14-firebase-adminsdk-mtbra-c35f8fbada.json")  # Reemplaza con el path a tu archivo JSON
firebase_app = initialize_app(cred, {"storageBucket": "angular-html-57b14.appspot.com"})  # Reemplaza con el bucket de tu proyecto

class FbConsult:
    
    def __init__(self):
        self.fb_storage = FbStorageService()



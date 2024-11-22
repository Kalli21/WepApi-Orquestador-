
from fastapi import File, UploadFile, HTTPException
from firebase_admin import storage
from urllib.parse import urlparse, unquote

import io
from datetime import datetime


class FbStorageService:
    
    carpeta = "Archivo/"
    
    async def upload_file(self, file: UploadFile = File(...)):
        try:
            # Obtener el bucket de Firebase Storage
            bucket = storage.bucket()

            # Crear un nombre único para el archivo (puedes personalizar esto)
            file_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
            file_name = self.carpeta + file_name
            blob = bucket.blob(file_name)

            # Leer el archivo y subirlo a Firebase
            content = await file.read()
            blob.upload_from_string(content, content_type=file.content_type)

            # # Hacer el archivo accesible públicamente (opcional)
            # blob.make_public()

            return {"message": "Archivo subido exitosamente", "url": blob.public_url}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al subir el archivo: {str(e)}")


    async def get_file(self, url):
        
        file_path = url.split("/")  # Elimina el '/' inicial
        file_path = file_path[-1]
        file_name = self.carpeta + file_path
        
        # Extraer el nombre del archivo de la URL
        bucket = storage.bucket()

        # Obtener el blob del archivo
        blob = bucket.blob(file_name)

        # Descargar el contenido del archivo en memoria
        contenido = blob.download_as_bytes()
        return io.BytesIO(contenido)

    
    async def eliminar_archivo_firebase(self, url):

        try:
           
            file_path = url.split("/")  # Elimina el '/' inicial
            file_path = file_path[-1]
            file_name = self.carpeta + file_path
            # Obtén el bucket de Firebase Storage
            bucket = storage.bucket()

            # Intenta localizar el archivo
            blob = bucket.blob(file_name)

            # Verificar si el archivo existe en el bucket
            if not blob.exists():
                return f"El archivo '{file_path}' no existe en el bucket."

            # Eliminar el archivo
            blob.delete()
            return f"El archivo '{file_path}' ha sido eliminado exitosamente."

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al subir el archivo: {str(e)}")




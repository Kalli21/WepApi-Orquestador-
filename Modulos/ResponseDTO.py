from pydantic import BaseModel
from typing import List, Optional, Any

# Modelo para estructurar la respuesta del servicio .NET
class ResponseDTO(BaseModel):
    isSuccess: bool = True
    result: Optional[Any] = None
    displayMessage: Optional[str] = None
    errorMessages: Optional[List[str]] = None
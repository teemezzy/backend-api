from typing import Any, Optional
from pydantic import BaseModel


class GenericResponse(BaseModel):
    message: str
    user: Optional[Any] = None
    error_code: int
    details: Optional[dict] = {}
    
    


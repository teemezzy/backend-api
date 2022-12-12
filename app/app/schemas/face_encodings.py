from pydantic import BaseModel
from uuid import UUID
from typing import Dict

class FaceEncodingsBase(BaseModel):
    user_id: UUID
    face_encoding: Dict

class FaceEncodingsUpdate(BaseModel):
    face_encoding: Dict
    
class FaceEncodingsCreate(BaseModel):
    user_id: UUID
    face_encoding: Dict

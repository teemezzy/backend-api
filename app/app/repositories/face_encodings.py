from typing import List, Optional
from uuid import UUID
from app.schemas import FaceEncodingsCreate, FaceEncodingsUpdate
from app.models.face_encodings import FaceEncodings
from sqlalchemy.orm import Session
from app.repositories.base import BaseRepository

from app.core.logger_client import logger_client

logger = logger_client.getLogger(__name__)

class FaceEncodingsRepository(BaseRepository[FaceEncodings, FaceEncodingsCreate, FaceEncodingsUpdate]):

    def get_all_face_encodings(self, db: Session) -> Optional[List[FaceEncodings]]:
        return (
            db.query(FaceEncodings)
            .filter(FaceEncodings.face_encoding != None)
            .all()
        )
        
    def create(self, db: Session, obj_in: FaceEncodingsCreate) -> FaceEncodings:
        face_encodings_in = FaceEncodings(
            user_id=obj_in.user_id,
            face_encoding=obj_in.face_encoding
        )
        db.add(face_encodings_in)
        db.commit()
        db.refresh(face_encodings_in)
        return face_encodings_in

    def get_face_encodings_by_user_id(self, db: Session, user_id: UUID) -> Optional[FaceEncodings]:
        return (
            db.query(FaceEncodings)
            .filter(FaceEncodings.user_id == user_id)
            .first()
        )
        
face_encodings_repository = FaceEncodingsRepository(FaceEncodings)

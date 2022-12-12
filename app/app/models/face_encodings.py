from app.db.base_class import Base
from typing import TYPE_CHECKING, Dict
from sqlalchemy import  Column
from sqlalchemy import ForeignKey, Column
from sqlalchemy.dialects.postgresql import UUID, JSON
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from .user import User  # noqa: F401


class FaceEncodings(Base):
    __tablename__ = "face_encodings"
    face_encoding: Dict = Column(JSON, nullable=False)
    user_id: str = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    user: "User" = relationship("User")
    

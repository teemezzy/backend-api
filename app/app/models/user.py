from app.db.base_class import Base

from sqlalchemy import Boolean, Column, String

class User(Base):
    __tablename__ = "users"
    first_name: str = Column(String, nullable=False)
    last_name: str = Column(String, nullable=False)
    email: str = Column(String, nullable=False, unique=True)
    hashed_password: str = Column(String, nullable=False)
    is_active: bool = Column(Boolean, default=True)
    is_superuser: bool = Column(Boolean, default=False)
    is_verified: bool = Column(Boolean, default=False)
    
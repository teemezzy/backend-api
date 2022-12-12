from typing import Optional
from uuid import UUID
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.schemas import UserCreate, UserBase
from app.models import User
from app.repositories import user_repository

class UserService:
    
    def get(self, db: Session, id: UUID) -> Optional[User]:
        return user_repository.get(db, id)
    
    def create(self, db: Session, user_in: UserCreate) -> UserBase:
        if user_in.password != user_in.verify_password:
            raise HTTPException(status_code=400, detail="Passwords do not match")

        if user_repository.get_by_email(db, user_in.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        
        return user_repository.create(db, user_in)
    
    def update_face_encodings(self, db: Session, user_id: UUID, encrypted_encodings: bytes):
        return user_repository.update_face_encodings(db, user_id, encrypted_encodings)
    
    def get_by_email(self, db: Session, email: str):
        return user_repository.get_by_email(db, email)
    
    def authenticate(self, db: Session, email: str, password: str):
        return user_repository.authenticate(db, email, password)
    
    def is_active(self, user: User):
        return user_repository.is_active(user)
    
    
    
user_service = UserService()

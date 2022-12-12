import datetime
from typing import Optional
from uuid import UUID
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import verify_password, get_password_hash
from sqlalchemy.orm import Session
from app.core.logger_client import logger_client

from app.repositories.base import BaseRepository

logger = logger_client.getLogger(__name__)

class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    def get(self, db: Session, id: UUID) -> Optional[User]:
        return db.query(User).get(id)
        
    def create(self, db: Session, user_in: UserCreate) -> User:
                
        db_user = User(
            first_name=user_in.first_name,
            last_name=user_in.last_name,
            email=user_in.email,
            hashed_password=get_password_hash(user_in.password),
            is_active=True,
            is_superuser=False,
            is_verified=False,
        )
        db_user.created_at = datetime.datetime.now()
        db_user.updated_at = datetime.datetime.now()
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    
    def get_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()
    
    def authenticate(self, db: Session, email: str, password: str):
        user = self.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    def is_active(self, user: User):
        return user.is_active
    
    def is_superuser(self, user: User):
        return user.is_superuser

        
    
    

user_repository = UserRepository(User)

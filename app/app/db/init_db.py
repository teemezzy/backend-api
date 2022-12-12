from sqlalchemy.orm import Session

from app import schemas, repositories
from app.db import base
from app.core.config import settings


def init_db(db: Session) -> None:
    user = repositories.user_repository.get_by_email(db, email=settings.FIRST_USER_EMAIL)
    if not user:
        user = schemas.UserCreate(
            first_name="John",
            last_name="Doe",
            email=settings.FIRST_USER_EMAIL,
            password=settings.FIRST_USER_PASSWORD,
            verify_password=settings.FIRST_USER_PASSWORD,
            is_active=True,
            is_superuser=True,
            is_verified=True,
        )
        user = repositories.user_repository.create(db, user)
    

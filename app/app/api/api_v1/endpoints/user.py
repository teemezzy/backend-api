from typing import Any
from app.schemas import GenericResponse, LoggedInUser, UserCreate
from app.services import user_service, face_encodings_service
from app.services.response_formatter import response_content_formatter
from app.models import User
from app.api import deps
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends, Response
from fastapi.responses import JSONResponse


router = APIRouter()

@router.post("/register", response_model=GenericResponse)
async def register(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
) -> Any:
    """
    User registration endpoint
    """
    
    user_service.create(db, user_in)
    return JSONResponse(
        content=response_content_formatter.get_response_by_code(0),
        status_code=200
    )
        


@router.get("/me", response_model=LoggedInUser)
async def get_current_user(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    
    has_activated_face_id = face_encodings_service.get_face_encodings_by_user_id(db, current_user.id)
    userToReturn = LoggedInUser(
        id=current_user.id,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        email=current_user.email,
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser,
        is_verified=current_user.is_verified,
        has_activated_face_id=has_activated_face_id is not None
    )
    
    return userToReturn




@router.get("/logout", response_model=GenericResponse)
def logout(
    response: Response,
) -> Any:
    """
    Log out - removes JWT cookie
    """
    response.delete_cookie("token")
    return JSONResponse(
        content=response_content_formatter.get_response_by_code(0),
        status_code=200
    )

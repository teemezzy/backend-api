from typing import Any
from fastapi import APIRouter, UploadFile, Depends
from fastapi.responses import JSONResponse
from app.schemas import GenericResponse
from app.services import face_encodings_service
from app.services import face_liveness_service
from app.services.response_formatter import response_content_formatter
from app.services.face_comparison import face_comparison_service
from app.models import User
from app.api import deps

from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/register/face-id", response_model=GenericResponse)
async def register_face_id(
    *,
    db: Session = Depends(deps.get_db),
    file: UploadFile,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Registration endpoint
    """
    # check if the file is a valid video file
    if not file.content_type.startswith("video"):
        return JSONResponse(
            status_code=400,
            content=response_content_formatter.get_response_by_code(1, {"message": "Invalid video feed: Video feed not a valid file type"}),
        )
    user_video_feed = file.file.read()
    
    if not face_liveness_service.is_live_face(user_video_feed):
        reponse_content = response_content_formatter.get_response_by_code(2)
        return JSONResponse(content=reponse_content, status_code=406)
    
    face_encodings_service.encode_face(db, user_video_feed, current_user)
    return JSONResponse(
            content=response_content_formatter.get_response_by_code(0),
            status_code=200
    )

@router.post("/verify/face-id", response_model=GenericResponse)
async def verify(
    *,
    db: Session = Depends(deps.get_db),
    file: UploadFile,
) -> Any:
    """
    Verification endpoint
    """
    if not file.content_type.startswith("video"):
        return JSONResponse(
            status_code=400,
            content=response_content_formatter.get_response_by_code(1, {"message": "Invalid video feed: Video feed not a valid file type"}),
        )
    
    user_video_feed = file.file.read()
    
    if not face_liveness_service.is_live_face(user_video_feed):
        reponse_content = response_content_formatter.get_response_by_code(2)
        return JSONResponse(content=reponse_content, status_code=406)

    return face_encodings_service.verify_user_face(db, user_video_feed)


@router.post("/liveness/check", response_model=GenericResponse)
async def check_liveness(
    *,
    file: UploadFile,
    current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Liveness check endpoint
    """
    if not file.content_type.startswith("video"):
        return JSONResponse(
            status_code=400,
            content=response_content_formatter.get_response_by_code(1, {"message": "Invalid video feed: Video feed not a valid file type"}),
        )
    
    user_video_feed = file.file.read()
    
    if not face_liveness_service.is_live_face(user_video_feed):
        reponse_content = response_content_formatter.get_response_by_code(2)
        return JSONResponse(content=reponse_content, status_code=406)
    
    return JSONResponse(
            content=response_content_formatter.get_response_by_code(7),
            status_code=200
    )


@router.post("/comparison/check", response_model=GenericResponse)
async def check_comparison(
    *,
    db: Session = Depends(deps.get_db),
    file: UploadFile,
    id_document: UploadFile,
    # current_user: User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Comparison check endpoint
    """
    if not file.content_type.startswith("video"):
        return JSONResponse(
            status_code=400,
            content=response_content_formatter.get_response_by_code(1, {"message": "Invalid video feed: Video feed not a valid file type"}),
        )
    
    if not id_document.content_type.startswith("image"):
        return JSONResponse(
            status_code=400,
            content=response_content_formatter.get_response_by_code(1, {"message": "Invalid ID document: ID document not a valid file type"}),
        )
    
    response = face_comparison_service.compare_face_with_id(db, file, id_document)
    
    return JSONResponse(
            content=response_content_formatter.get_response_by_code(0, details=response),
            status_code=200
    )

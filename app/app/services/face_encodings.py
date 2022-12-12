from typing import List, Optional, Any
from app.core.security import decrypt_encodings, encrypt_encodings
from app.schemas import LoggedInUser, FaceEncodingsCreate
from app.repositories import face_encodings_repository
from app.services import user_service
from app.services.response_formatter import response_content_formatter
from app.models import User, FaceEncodings
from sqlalchemy.orm import Session
import tempfile
import uuid
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

import cv2
import face_recognition

from app.core.logger_client import logger_client

logger = logger_client.getLogger(__name__)

class FaceEncodingsService:
    
    def get_face_encodings_by_user_id(self, db: Session, user_id: uuid.UUID) -> Optional[FaceEncodings]:
        return face_encodings_repository.get_face_encodings_by_user_id(db, user_id)

    def get_all_face_encoding_info(self, db: Session) -> Optional[List[FaceEncodings]]:
        face_encoding_results = face_encodings_repository.get_all_face_encodings(db=db)
        face_encodings = []
        user_ids = []
        
        if face_encoding_results:
            for face_encoding_result in face_encoding_results:
                face_encodings.append(decrypt_encodings(face_encoding_result.face_encoding.get("encoding")))
                user_ids.append(face_encoding_result.user_id)

            return {"face_encodings": face_encodings, "user_ids": user_ids}
        else:
            return {"face_encodings": [], "user_ids": []}

    def verify_user_face(self, db: Session, user_video_feed: Any):
        # TODO: Preload the face encodings from the database
        face_encoding_info = self.get_all_face_encoding_info(db)
        known_face_encodings = face_encoding_info.get("face_encodings")
        known_face_ids = face_encoding_info.get("user_ids")
        
        identified_ids = []
        try:
            with tempfile.NamedTemporaryFile(prefix=f"{uuid.uuid4()}", suffix=".mp4") as temp_video:
                temp_video.write(user_video_feed)

                num_of_frames = 0
                cap = cv2.VideoCapture(temp_video.name)

                while cap.isOpened():
                    # TODO: This is a temporary fix to only process 1 frame
                    # We need to process more than one frame and average the results
                    if num_of_frames == 4:
                        break

                    ret, frame = cap.read()
                    if ret == False:
                        break

                    rgb_frame = frame[:, :, ::-1]
                    # rotate the frame 180 degrees to match the orientation of the video
                    # This is to correct videos captured from the front camera as the metadata is not used
                    # See https://stackoverflow.com/questions/44380432/opencv-video-looks-good-but-frames-are-rotated-90-degrees
                    # rgb_frame = cv2.rotate(rgb_frame, cv2.ROTATE_180)
                    # cv2.imwrite("ver-frame.jpg", rgb_frame)
                    boxes = face_recognition.face_locations(rgb_frame)
                    encodings = face_recognition.face_encodings(rgb_frame, boxes)

                    for encoding in encodings:
                        matches = face_recognition.compare_faces(
                            known_face_encodings, encoding, tolerance=0.95)
                        user_id = "Unknown"
                        if True in matches:
                            first_match_index = matches.index(True)
                            user_id = known_face_ids[first_match_index]
                            identified_ids.append(user_id)

                    num_of_frames += 1

                cap.release()

                if len(set(identified_ids)) == 1:
                    authenticated_user = user_service.get(db, identified_ids[0])

                    userToReturn = LoggedInUser(
                        id=authenticated_user.id,
                        first_name=authenticated_user.first_name,
                        last_name=authenticated_user.last_name,
                        email=authenticated_user.email,
                        is_active=authenticated_user.is_active,
                        is_superuser=authenticated_user.is_superuser,
                        is_verified=authenticated_user.is_verified,
                        has_activated_face_id=True,
                    )
                    
                    return JSONResponse(
                        status_code=200,
                        content=response_content_formatter.get_response_by_code(
                            0,
                            user = jsonable_encoder(userToReturn)
                        )
                    )
                else:
                    return JSONResponse(
                        status_code=406,
                        content=response_content_formatter.get_response_by_code(
                            4,
                            details={"message": "Face verification failed. Please try again. If you're a new user, please register first."}
                        )
                    )
        except Exception as e:
            logger.error(f"Error: {e}")
            return JSONResponse(
                status_code=500,
                content=response_content_formatter.get_response_by_code(
                    1,
                    details={"message": "Face verification failed. Please try again."}
                )
            )

    def encode_face(self, db: Session, user_video_feed: Any, current_user: User = None):
        """
        Encode face video 
        """
        # encodings = []
        final_encoding = None
        with tempfile.NamedTemporaryFile(prefix=f"{uuid.uuid4()}", suffix=".mp4") as temp_video:
            # temp_video.write(file.file.read())
            temp_video.write(user_video_feed)

            num_of_frames = 0
            cap = cv2.VideoCapture(temp_video.name)

            while(cap.isOpened()):
                # TODO: This is a temporary fix to only process 1 frame
                # We need to process more than one frame and average the results
                if num_of_frames == 5:
                    break

                ret, frame = cap.read()
                if ret == False:
                    break

                rgb_frame = frame[:, :, ::-1]
                # rotate the frame 180 degrees to match the orientation of the video
                # This is to correct videos captured from the front camera as the metadata is not used
                # See https://stackoverflow.com/questions/44380432/opencv-video-looks-good-but-frames-are-rotated-90-degrees
                # rgb_frame = cv2.rotate(rgb_frame, cv2.ROTATE_180)
                # cv2.imwrite("frame.jpg", rgb_frame)

                boxes = face_recognition.face_locations(rgb_frame)
                # encodings.append(face_recognition.face_encodings(rgb_frame, boxes)[0])
                encoding = face_recognition.face_encodings(rgb_frame, boxes)
                if encoding:
                    final_encoding = encoding[0]
                    break

                num_of_frames += 1

            cap.release()

        # encrypted_encodings = encrypt_encodings(encodings)
        encrypted_encodings = encrypt_encodings(final_encoding)
        face_obj_in = FaceEncodingsCreate(
            user_id=current_user.id,
            face_encoding={"encoding": encrypted_encodings}
        )
        face_encodings_repository.create(db, obj_in=face_obj_in)


face_encodings_service = FaceEncodingsService()

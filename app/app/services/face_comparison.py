
import tempfile
import uuid
import cv2
from typing import Any
from sqlalchemy.orm import Session
from deepface import DeepFace
from app.core.logger_client import logger_client
from fastapi import UploadFile
from PIL import Image
from io import BytesIO

from tensorflow.keras.preprocessing.image import img_to_array

logger = logger_client.getLogger(__name__)

class FaceComparisonService:
    
    def __init__(self):
        pass
    
    
    def compare_face_with_id(self, db: Session, file: UploadFile, id_document: UploadFile) -> Any:
        """
        Compare face with ID document
        """
        comparison_result = {
            "is_the_same_person": False,
            "has_error": False,
            "error_message": ""
        }
        
        try:
            with tempfile.NamedTemporaryFile(prefix=f"{uuid.uuid4()}", suffix=".mp4") as temp_video:
                temp_video.write(file.file.read())
                images_to_compare_against = 0
                            
                cap = cv2.VideoCapture(temp_video.name)
                
                with tempfile.NamedTemporaryFile(prefix=f"{uuid.uuid4()}", suffix=".jpg") as temp_id_document:
                    id_document_image = img_to_array(Image.open(BytesIO(id_document.file.read())))
                    cv2.imwrite(temp_id_document.name, id_document_image)
                    
                    comparision_results = []
                    while cap.isOpened() and images_to_compare_against < 4:
                        ret, frame = cap.read()
                        if ret == False:
                            break
                        
                        rgb_frame = frame[:, :, ::-1]

                        # rotate the frame 180 degrees to match the orientation of the video
                        # This is to correct videos captured from the front camera as the metadata is not used
                        # See https://stackoverflow.com/questions/44380432/opencv-video-looks-good-but-frames-are-rotated-90-degrees
                        # rgb_frame = cv2.rotate(rgb_frame, cv2.ROTATE_180)
                        with tempfile.NamedTemporaryFile(prefix=f"{uuid.uuid4()}", suffix=".jpg") as temp_frame:
                            cv2.imwrite(temp_frame.name, rgb_frame)
                            result = DeepFace.verify(img1_path=temp_id_document.name, img2_path=temp_frame.name, model_name="Facenet")
                            
                            comparision_results.append(result.get("verified"))
                            images_to_compare_against += 1

            comparison_result["is_the_same_person"] = all(comparision_results)
            return comparison_result
                    
        except Exception as e:
            logger.error(f"Error comparing face with ID document: {e}")
            comparison_result["has_error"] = True
            comparison_result["error_message"] = "Error comparing face with ID document: Please try again"
            
            
            return comparison_result
                

            
            
            
        
    
    

face_comparison_service = FaceComparisonService()

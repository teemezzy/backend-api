from typing import Any
import tempfile
import uuid
import cv2

from app.core.logger_client import logger_client

import numpy as np 
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv3D, MaxPooling3D

from pathlib import Path

logger = logger_client.getLogger(__name__)

LIVENESS_MODEL_PATH = Path(__file__).parent / "artifact" / "models" / "model.h5"

class FaceLivenessService:
    def __init__(self):
        self.model = None
        
    def load_liveness_model(self):
        model = Sequential()
        model.add(Conv3D(32, kernel_size=(3, 3, 3),
                        activation='relu',
                        input_shape=(24,100,100,1)))
        model.add(Conv3D(64, (3, 3, 3), activation='relu'))
        model.add(MaxPooling3D(pool_size=(2, 2, 2)))
        model.add(Conv3D(64, (3, 3, 3), activation='relu'))
        model.add(MaxPooling3D(pool_size=(2, 2, 2)))
        model.add(Conv3D(64, (3, 3, 3), activation='relu'))
        model.add(MaxPooling3D(pool_size=(2, 2, 2)))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(2, activation='softmax'))

        model.load_weights(LIVENESS_MODEL_PATH)
        logger.info("Loaded liveness model")
        
        self.model = model
        
    def is_live_face(self, user_video_feed: Any):
        if not self.model:
            self.load_liveness_model()
            
        with tempfile.NamedTemporaryFile(prefix=f"{uuid.uuid4()}", suffix=".mp4") as temp_video:
            temp_video.write(user_video_feed)

            frames_to_predict = []
            liveness_truths = []
            
            cap = cv2.VideoCapture(temp_video.name)

            while(cap.isOpened() and len(frames_to_predict) < 24):
                if len(frames_to_predict) < 24:
                    
                    ret, frame = cap.read()
                    if ret == False:
                        break
                    
                    liveimg = cv2.resize(frame, (100,100))
                    liveimg = cv2.cvtColor(liveimg, cv2.COLOR_BGR2GRAY)
                    frames_to_predict.append(liveimg)
                else:
                    ret, frame = cap.read()
                    if ret == False:
                        break
                    
                    liveimg = cv2.resize(frame, (100,100))
                    liveimg = cv2.cvtColor(liveimg, cv2.COLOR_BGR2GRAY)
                    frames_to_predict.append(liveimg)
                    inp = np.array([frames_to_predict[-24:]])
                    inp = inp/255
                    inp = inp.reshape(1,24,100,100,1)
                    pred = self.model.predict(inp)
                    frames_to_predict = frames_to_predict[-25:]
                    if pred[0][0]> .95:
                        liveness_truths.append(True)
                    else:
                        liveness_truths.append(False)
            
            cap.release()
            
            is_live = all(liveness_truths)
            return is_live



face_liveness_service = FaceLivenessService()

from datetime import datetime, timedelta
from typing import Any, List, Union
from jose import jwt
from passlib.context import CryptContext
import pickle

import json
from json import JSONEncoder
import numpy

from app.core.config import settings


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"

def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def encrypt_encodings(encodings: List[Any]):
    # pickled_encodings = pickle.dumps(encodings)
    encoded_encodings = json.dumps(encodings, cls=NumpyArrayEncoder)
    # TODO: Encrypt the encodings 
    return encoded_encodings

def decrypt_encodings(encodings: Any) -> Any:
    # unpickled_encodings = pickle.loads(encodings)
    decoded_encodings = numpy.asarray(json.loads(encodings))
    # TODO: Decrypt the encodings
    return decoded_encodings

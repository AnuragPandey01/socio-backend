import os
import jwt
import time
from pydantic import BaseModel
from passlib.hash import bcrypt
from typing import Annotated
from fastapi import Depends, HTTPException,status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from database import SessionDep
from models.user import User

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXP = int(os.getenv("EXP"))

def create_token(user_id: str):
    payload = {"sub": user_id,"exp": time.time()+EXP}
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")

class Token(BaseModel):
    access_token: str


def hash_password(password):
    return bcrypt.hash(password)


def verify_password(password, hash):
    return bcrypt.verify(password, hash)


security = HTTPBearer()

def get_current_user(session: SessionDep,bearer : Annotated[HTTPAuthorizationCredentials,Depends(security)]):
    payload = verify_token(bearer.credentials)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    user = session.get(User,payload["sub"])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token")
    return user

UserDep = Annotated[User,Depends(get_current_user)]
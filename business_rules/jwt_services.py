from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import Union
from fastapi import Depends, HTTPException, status
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from os.path import normpath, join, dirname, abspath
from business_rules.view_models.jwt_dto import *
from business_rules.view_models.user_dto import UserInDB, UserBase
from model.user import User
from database_settings import get_db
import os

PROJECT_ROOT = dirname(dirname(abspath(__file__)))
SECRET_FILE = normpath(join(PROJECT_ROOT, 'SECRET.key'))
SECRET_KEY = open(SECRET_FILE).read().strip()
ALGORITHM = os.environ.get("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user_by_username(username: str) -> UserInDB:
    db = list(get_db())[0]
    user_db = db.query(User).where(User.user_name == username).first()
    return user_db

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str, *args, **kwargs):
    user = get_user_by_username(username=username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user: UserBase = Depends(get_current_user)):
    if current_user.is_active is not True:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
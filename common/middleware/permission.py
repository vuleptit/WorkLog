import sys
import inspect
from functools import wraps
from business_rules.view_models.user_dto import *
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from business_rules.view_models.jwt_dto import TokenData
from common.const import *
from business_rules.jwt_services import get_user_by_username

def IsAuthenticated(func):
    print(inspect.signature(func))
    @wraps(func)
    def is_authenticated(*args, **kwargs):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            req = kwargs['request']
            token_key = req.headers['authorization'].split()[1]
            payload = jwt.decode(token_key, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
        except JWTError:
            raise credentials_exception
        except Exception as ex:
            raise HTTPException(detail="Not provided credentials", status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        
        # User Role
        user = get_user_by_username(username=token_data.username)
        if user is None:
            raise 
        if user.is_active is not True:
            raise HTTPException(detail="User not active", status_code=status.HTTP_401_UNAUTHORIZED)
        return func(*args, **kwargs)
    return is_authenticated
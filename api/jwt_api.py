from datetime import timedelta
from fastapi import APIRouter
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import  OAuth2PasswordRequestForm
from typing_extensions import Annotated
from business_rules.view_models.user_dto import UserBase
from business_rules.jwt_services import *
from database_settings import get_db

router = APIRouter()

@router.post("/access_token/", response_model=Token)
async def login_for_access_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    print(request.headers)
    user = authenticate_user(username = form_data.username, password = form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.user_name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=UserBase)
async def read_users_me(
    request: Request,
    current_user: UserBase = Depends(get_current_active_user),
):
    print(request.headers['authorization'].replace('Bearer','').strip())
    return current_user

@router.get("/users/me/items/")
async def read_own_items(
    current_user: Union[UserBase, str] = Depends(get_current_active_user)
):
    return [{"item_id": "Foo", "owner": current_user.user_name}]
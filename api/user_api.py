from fastapi import APIRouter, Depends, status, Response
from business_rules.user_services import *
from database_settings import get_db
from api.utils.custom_response import ResponseModel
import json

router = APIRouter()

@router.get('/{id}', response_model=ResponseModel)
def get_user(id: int, db: Session = Depends(get_db)) -> UserBase:
    user = get_user_by_id(db=db, user_id=id)
    print(dir(user))
    return ResponseModel(
        message = "Get User successfully",
        data = user,
        status = status.HTTP_200_OK
    )


@router.post('/register/')
def register(user_data: UserCreate, db: Session = Depends(get_db)) -> UserBase:
    result = create_or_update_user(db=db, user_data=user_data)
    return result


@router.post('/remove/{id}')
def register(id: int, db: Session = Depends(get_db)) -> UserBase:
    result = delete_user(db=db, user_id=id)
    return result
from fastapi import APIRouter, Depends, status, Response
from business_rules.user_services import *
from database_settings import get_db
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
router = APIRouter()

@router.get('/{id}')
def get_user(id: int, db: Session = Depends(get_db)) -> UserBase:
    result = get_user_by_id(db=db, user_id=id)
    return result

@router.post('/register/')
def register(user_data: UserCreate, db: Session = Depends(get_db)) -> UserBase:
    result = create_user(db=db, user_data=user_data)
    return result

@router.put('/update/')
def update(user_data: UserUpdate, db: Session = Depends(get_db)) -> UserBase:
    print("asdfasdfasd")
    result = update_user(db=db, user_data=user_data)
    return result

@router.post('/remove/{id}')
def remove(id: int, db: Session = Depends(get_db)) -> UserBase:
    result = delete_user(db=db, user_id=id)
    return result
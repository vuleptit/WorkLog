from fastapi import APIRouter, Depends, Form, Response, responses, Request
from fastapi.responses import JSONResponse, ORJSONResponse
from business_rules.user_services import *
from database_settings import get_db
from api.utils.custom_response import CustomResponse
from fastapi import HTTPException

router = APIRouter()

@router.get('/all')
def get_user(db: Session = Depends(get_db)):
    result = get_all_users(db=db)
    return result

@router.get('/{id}')
def get_user(id: int, db: Session = Depends(get_db)):
    result = get_user_by_id(db=db, user_id=id)
    return result

@router.post('/register/')
def register(user_data: UserInDB, db: Session = Depends(get_db)):
    result = create_user(db=db, user_data=user_data)
    return result

@router.put('/update/')
def update(response: Response, user_data: UserUpdate, db: Session = Depends(get_db)):
    result = update_user(db=db, user_data=user_data)
    # response.status_code = result.status
    return result

@router.post('/remove/{id}')
def remove(id: int, db: Session = Depends(get_db)):
    result = delete_user(db=db, user_id=id)
    return result

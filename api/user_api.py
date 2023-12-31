from fastapi import APIRouter, Depends

from business_rules.user_services import *
from database_settings import get_db

router = APIRouter()

@router.get('/{id}')
def get_user(id: int, db: Session = Depends(get_db)) -> UserBase:
    user = get_user_by_id(db=db, user_id=id)
    return user


@router.post('/register')
def register(user_data: UserCreate, db: Session = Depends(get_db)) -> UserBase:
    result = create_or_update_user(db=db, user_data=user_data)
    return result

from fastapi import APIRouter, Depends

from business_rules.user_services import *
from database_settings import get_db

router = APIRouter()


@router.post('/new/')
def register(user_data: UserCreate, db: Session = Depends(get_db)) -> UserBase:
    result = create_or_update_user(db=db, user_data=user_data)
    return result


@router.post('/remove/{id}')
def register(id: int, db: Session = Depends(get_db)) -> UserBase:
    result = delete_user(db=db, user_id=id)
    return result
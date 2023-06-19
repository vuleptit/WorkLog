from fastapi import APIRouter, Depends, Form
from business_rules.user_services import *
from database_settings import get_db

router = APIRouter()

@router.get('/{id}')
def get_user(id: int, db: Session = Depends(get_db)) -> UserBase:
    result = get_user_by_id(db=db, user_id=id)
    return result

@router.post('/register/')
def register(user_data: UserInDB, db: Session = Depends(get_db)) -> UserBase:
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

@router.post('/test/')
async def test(name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    # Handle the submitted form data here
    # For example, you could send an email or add it to a database
    return name

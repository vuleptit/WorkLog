from fastapi import APIRouter, Depends, Response, Request
from business_rules.setting_service import *
from database_settings import get_db
from common.middleware.permission import IsAuthenticated
router = APIRouter()


@router.get('/all/')
@IsAuthenticated
def get_setting(request: Request, response: Response, db: Session = Depends(get_db)):
    result = get_all_settings(db=db)
    response.status_code = result.status
    return result

@router.get('/{id}')
def get_setting(id: int, db: Session = Depends(get_db)):
    result = get_setting_by_id(db=db, setting_id=id)
    return result

@router.post('/create/')
def register(setting_data: SettingCreate, db: Session = Depends(get_db)):
    result = create_setting(db=db, setting_data=setting_data)
    return result

@router.put('/update/{id}')
def register(setting_data: SettingUpdate, db: Session = Depends(get_db)):
    result = update_setting(db=db, setting_data=setting_data)
    return result

@router.post('/remove/{id}')
def register(id: int, db: Session = Depends(get_db)):
    result = delete_setting(db=db, setting_id=id)
    return result
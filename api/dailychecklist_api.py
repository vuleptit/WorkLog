from fastapi import APIRouter, Depends, Response
from business_rules.daily_checklist_service import *
from database_settings import get_db

router = APIRouter()

@router.get('/all/')
def get_daily_checklist(response: Response, db: Session = Depends(get_db)):
    result = get_all_daily_checklists(db=db)
    response.status_code = result.status
    return result

@router.get('/{id}')
def get_daily_checklist(id: int, db: Session = Depends(get_db)):
    result = get_daily_checklist_by_id(db=db, daily_checklist_id=id)
    return result

@router.post('/create/')
def register(daily_checklist_data: DailyChecklistCreate, db: Session = Depends(get_db)):
    result = create_daily_checklist(db=db, daily_checklist_data=daily_checklist_data)
    return result

@router.put('/update/{id}')
def register(daily_checklist_data: DailyChecklistUpdate, db: Session = Depends(get_db)):
    result = update_daily_checklist(db=db, daily_checklist_data=daily_checklist_data)
    return result

@router.post('/remove/{id}')
def register(id: int, db: Session = Depends(get_db)):
    result = delete_daily_checklist(db=db, daily_checklist_id=id)
    return result
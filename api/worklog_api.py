from fastapi import APIRouter, Depends, Response, Request
from business_rules.work_logging_service import *
from database_settings import get_db
from common.middleware.permission import IsAuthenticated
router = APIRouter()

@router.get('/all/')
@IsAuthenticated
def get_work_logging(request: Request, response: Response, db: Session = Depends(get_db)):
    result = get_all_work_loggings(db=db)
    response.status_code = result.status
    return result

@router.get('/{id}')
def get_work_logging(id: int, db: Session = Depends(get_db)):
    result = get_work_logging_by_id(db=db, work_logging_id=id)
    return result

@router.post('/create/')
def register(work_logging_data: WorkLoggingCreate, db: Session = Depends(get_db)):
    result = create_work_logging(db=db, work_logging_data=work_logging_data)
    return result

@router.put('/update/{id}')
def register(work_logging_data: WorkLoggingUpdate, db: Session = Depends(get_db)):
    result = update_work_logging(db=db, work_logging_data=work_logging_data)
    return result

@router.post('/remove/{id}')
def register(id: int, db: Session = Depends(get_db)):
    result = delete_work_logging(db=db, work_logging_id=id)
    return result
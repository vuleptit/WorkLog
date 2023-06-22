from fastapi import APIRouter, Depends, Response
from business_rules.task_service import *
from database_settings import get_db

router = APIRouter()

@router.get('/all/')
def get_task(response: Response, db: Session = Depends(get_db)):
    result = get_all_tasks(db=db)
    response.status_code = result.status
    return result

@router.get('/{id}')
def get_task(id: int, db: Session = Depends(get_db)):
    result = get_task_by_id(db=db, task_id=id)
    return result

@router.post('/create/')
def register(task_data: TaskCreate, db: Session = Depends(get_db)):
    result = create_task(db=db, task_data=task_data)
    return result

@router.put('/update/{id}')
def register(task_data: TaskUpdate, db: Session = Depends(get_db)):
    result = update_task(db=db, task_data=task_data)
    return result

@router.post('/remove/{id}')
def register(id: int, db: Session = Depends(get_db)):
    result = delete_task(db=db, task_id=id)
    return result
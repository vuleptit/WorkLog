from fastapi import APIRouter, Depends

from business_rules.task_service import *
from database_settings import get_db

router = APIRouter()

@router.get('/{id}')
def get_task(id: int, db: Session = Depends(get_db)) -> TaskBase:
    task = get_task_by_id(db=db, task_id=id)
    return task


@router.post('/new/')
def register(task_data: TaskBase, db: Session = Depends(get_db)) -> TaskBase:
    result = create_or_update_task(db=db, task_data=task_data)
    return result


@router.post('/remove/{id}')
def register(id: int, db: Session = Depends(get_db)) -> TaskBase:
    result = delete_task(db=db, task_id=id)
    return result
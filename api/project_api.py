from fastapi import APIRouter, Depends, Form, Request, Response

from business_rules.project_service import *
from database_settings import get_db

router = APIRouter()

@router.get('/all/')
def get_project(response: Response, db: Session = Depends(get_db)) -> ProjectBase:
    result = get_all_projects(db=db)
    response.status_code = result.status
    return result

@router.get('/{id}')
def get_project(id: int, db: Session = Depends(get_db)) -> ProjectBase:
    result = get_project_by_id(db=db, project_id=id)
    return result

@router.post('/create/')
def register(project_data: ProjectBase, db: Session = Depends(get_db)) -> ProjectBase:
    result = create_project(db=db, project_data=project_data)
    return result

@router.put('/update/{id}')
def register(id: int, db: Session = Depends(get_db)) -> ProjectBase:
    result = update_project(db=db, project_id=id)
    return result

@router.post('/remove/{id}')
def register(id: int, db: Session = Depends(get_db)) -> ProjectBase:
    result = delete_project(db=db, project_id=id)
    return result
from fastapi import APIRouter, Depends

from business_rules.project_service import *
from database_settings import get_db

router = APIRouter()

@router.get('/{id}')
def get_project(id: int, db: Session = Depends(get_db)) -> ProjectBase:
    project = get_project_by_id(db=db, project_id=id)
    return project


@router.post('/create/')
def register(project_data: ProjectBase, db: Session = Depends(get_db)) -> ProjectBase:
    result = create_or_update_project(db=db, project_data=project_data)
    return result


@router.post('/remove/{id}')
def register(id: int, db: Session = Depends(get_db)) -> ProjectBase:
    result = delete_project(db=db, project_id=id)
    return result
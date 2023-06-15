from sqlalchemy.orm import Session

from model.project import *
from business_rules.view_models.project_dto import *

def get_project_by_id(db: Session, project_id: int):
    project_query = db.query(Project).where(Project.id == project_id)
    return project_query.first()

def create_or_update_project(db: Session, project_data: ProjectBase):
    if project_data.id <= 0:
        # Create new Project
        project_item = Project()
        update_fields = ["id", "name", "code_on_jira"]
        for field in update_fields:
            setattr(project_item, field, getattr(project_data, field))
        db.add(project_item)
        db.commit()
        db.refresh(project_item)
        return project_item
    else:
        # Update
        project_in_db = get_project_by_id(db=db, project_id=project_data.id)
        update_fields = ["id", "name", "code_on_jira"]
        for field in update_fields:
            setattr(project_item, field, getattr(project_data, field))
        db.commit()
        db.refresh(project_in_db)
        print(type(project_in_db))
        print(project_in_db)
        return project_in_db

def delete_project(db: Session, project_id: int):
    project_query = db.query(Project).where(Project.id == project_id).first()
    db.delete(project_query)
    db.commit()
    project_in_db = get_project_by_id(db=db, project_id=project_id)
    return project_in_db
    
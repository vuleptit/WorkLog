from sqlalchemy.orm import Session

from model.task import *
from business_rules.view_models.task_dto import *

def get_task_by_id(db: Session, task_id: int):
    task_query = db.query(Task).where(Task.id == task_id)
    return task_query.first()

def create_or_update_task(db: Session, task_data: TaskBase):
    if task_data.id <= 0:
        # Create new Task
        task_item = Task()
        update_fields = ["name", "project_id", "code_on_jira"]
        for field in update_fields:
            setattr(task_item, field, getattr(task_data, field))
        db.add(task_item)
        db.commit()
        db.refresh(task_item)
        return task_item
    else:
        # Update
        task_in_db = get_task_by_id(db=db, task_id=task_data.id)
        update_fields = ["name", "project_id", "code_on_jira"]
        for field in update_fields:
            setattr(task_item, field, getattr(task_data, field))
        db.commit()
        db.refresh(task_in_db)
        print(type(task_in_db))
        print(task_in_db)
        return task_in_db

def delete_task(db: Session, task_id: int):
    task_query = db.query(Task).where(Task.id == task_id).first()
    db.delete(task_query)
    db.commit()
    task_in_db = get_task_by_id(db=db, task_id=task_id)
    return task_in_db
    
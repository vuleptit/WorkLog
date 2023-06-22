from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import exc
from model.task import *
from business_rules.view_models.task_dto import *
from api.utils.custom_response import CustomResponse
from fastapi import status

def get_all_tasks(db: Session):
    tasks = db.query(Task).all()
    message = "Successful"
    response = CustomResponse(
        message=message,
        data=tasks,
        status=status.HTTP_200_OK
    )
    return response

def get_task_by_id(db: Session, task_id: int):
    try:
        task= db.query(Task).where(Task.id == task_id).first()
    
        if task is not None:
            return CustomResponse(
                message = "Successfully",
                data = task.__dict__,
                status = status.HTTP_200_OK
            )
        else:
            return CustomResponse(
                message = f"Task with id {task_id} does not exist",
                status = status.HTTP_400_BAD_REQUEST
            )
    except Exception as ex:
        return HTTPException(detail="Something went wrong", status_code=status.HTTP_410_GONE)

def update_task(db: Session, task_data: TaskUpdate):
    try:
        task_in_db = db.query(Task).where(Task.id == task_data.id).first()
        if task_in_db is None:
            return CustomResponse(
                message = "Failed",
                exception = f"Task with id {task_data.id} does not exist",
                status = status.HTTP_400_BAD_REQUEST
            )
        update_fields = task_data.dict()
        for field in update_fields.keys():
            setattr(task_in_db, field, getattr(task_data, field))
        db.commit()
        db.refresh(task_in_db)
        response = CustomResponse(
            message = "Successfully",
            data = task_in_db.__dict__,
            status = status.HTTP_201_CREATED
        )
        return response
    except exc.IntegrityError:
        return CustomResponse(
            message = "Failed",
            status = status.HTTP_404_NOT_FOUND,
            exception = f"Task with name {task_data.name} already existed"
        )
    except Exception as ex:
        return HTTPException(detail="Something went wrong", status_code=status.HTTP_410_GONE)


def create_task(db: Session, task_data: TaskCreate):
    try:
        task_item = Task()
        create_fields = list(TaskCreate.__fields__.keys())
        for field in create_fields:
            setattr(task_item, field, getattr(task_data, field))
        db.add(task_item)
        db.commit()
        db.refresh(task_item)
        response = CustomResponse(
            message = "Successfully",
            data = task_item.__dict__,
            status = status.HTTP_200_OK
        )
        return response
    except exc.IntegrityError:
        response = CustomResponse(
            message = "Failed",
            status = status.HTTP_404_NOT_FOUND,
            exception = f"task with name {task_data.name} already exist"
        )
        return response
    except Exception as ex:
        return HTTPException(detail="Something went wrong", status_code=status.HTTP_410_GONE)

def delete_task(db: Session, task_id: int):
    try:
        task_query = db.query(Task).where(Task.id == task_id).first()
        if task_query is None:
            return CustomResponse(
                message = "Failed",
                status = status.HTTP_404_NOT_FOUND,
                exception = f"task with id {task_id} does not exist"
            )
        db.delete(task_query)
        db.commit()
        return CustomResponse(
                message = "Succesfully",
                status = status.HTTP_200_OK,
            )
    except Exception as ex:
        return HTTPException(detail="Something went wrong", status_code=status.HTTP_410_GONE)
        
    
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import exc
from model.work_logging import *
from business_rules.view_models.work_logging_dto import *
from api.utils.custom_response import CustomResponse
from fastapi import status

def get_all_work_loggings(db: Session):
    work_loggings = db.query(WorkLogging).all()
    message = "Successful"
    response = CustomResponse(
        message=message,
        data=work_loggings,
        status=status.HTTP_200_OK
    )
    return response

def get_work_logging_by_id(db: Session, work_logging_id: int):
    try:
        work_logging= db.query(WorkLogging).where(WorkLogging.id == work_logging_id).first()
    
        if work_logging is not None:
            return CustomResponse(
                message = "Successfully",
                data = work_logging.__dict__,
                status = status.HTTP_200_OK
            )
        else:
            return CustomResponse(
                message = f"WorkLogging with id {work_logging_id} does not exist",
                status = status.HTTP_400_BAD_REQUEST
            )
    except Exception as ex:
        return HTTPException(detail="Something went wrong", status_code=status.HTTP_410_GONE)

def update_work_logging(db: Session, work_logging_data: WorkLoggingUpdate):
    try:
        work_logging_in_db = db.query(WorkLogging).where(WorkLogging.id == work_logging_data.id).first()
        if work_logging_in_db is None:
            return CustomResponse(
                message = "Failed",
                exception = f"WorkLogging with id {work_logging_data.id} does not exist",
                status = status.HTTP_400_BAD_REQUEST
            )
        update_fields = work_logging_data.dict()
        for field in update_fields.keys():
            setattr(work_logging_in_db, field, getattr(work_logging_data, field))
        db.commit()
        db.refresh(work_logging_in_db)
        response = CustomResponse(
            message = "Successfully",
            data = work_logging_in_db.__dict__,
            status = status.HTTP_201_CREATED
        )
        return response
    except exc.IntegrityError:
        return CustomResponse(
            message = "Failed",
            status = status.HTTP_404_NOT_FOUND,
            exception = f"WorkLogging with name {work_logging_data.name} already existed"
        )
    except Exception as ex:
        return HTTPException(detail="Something went wrong", status_code=status.HTTP_410_GONE)


def create_work_logging(db: Session, work_logging_data: WorkLoggingCreate):
    try:
        work_logging_item = WorkLogging()
        create_fields = list(WorkLoggingCreate.__fields__.keys())
        for field in create_fields:
            setattr(work_logging_item, field, getattr(work_logging_data, field))
        db.add(work_logging_item)
        db.commit()
        db.refresh(work_logging_item)
        response = CustomResponse(
            message = "Successfully",
            data = work_logging_item.__dict__,
            status = status.HTTP_200_OK
        )
        return response
    except exc.IntegrityError:
        response = CustomResponse(
            message = "Failed",
            status = status.HTTP_404_NOT_FOUND,
            exception = f"work_logging with name {work_logging_data.name} already exist"
        )
        return response
    except Exception as ex:
        return HTTPException(detail="Something went wrong", status_code=status.HTTP_410_GONE)

def delete_work_logging(db: Session, work_logging_id: int):
    try:
        work_logging_query = db.query(WorkLogging).where(WorkLogging.id == work_logging_id).first()
        if work_logging_query is None:
            return CustomResponse(
                message = "Failed",
                status = status.HTTP_404_NOT_FOUND,
                exception = f"work_logging with id {work_logging_id} does not exist"
            )
        db.delete(work_logging_query)
        db.commit()
        return CustomResponse(
                message = "Succesfully",
                status = status.HTTP_200_OK,
            )
    except Exception as ex:
        return HTTPException(detail="Something went wrong", status_code=status.HTTP_410_GONE)
        
    
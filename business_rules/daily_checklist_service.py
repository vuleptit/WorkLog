from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import exc
from model.daily_checklist import *
from business_rules.view_models.daily_checklist_dto import *
from api.utils.custom_response import CustomResponse
from fastapi import status

def get_all_daily_checklists(db: Session):
    daily_checklists = db.query(DailyChecklist).all()
    message = "Successful"
    response = CustomResponse(
        message=message,
        data=daily_checklists,
        status=status.HTTP_200_OK
    )
    return response

def get_daily_checklist_by_id(db: Session, daily_checklist_id: int):
    try:
        daily_checklist= db.query(DailyChecklist).where(DailyChecklist.id == daily_checklist_id).first()
    
        if daily_checklist is not None:
            return CustomResponse(
                message = "Successfully",
                data = daily_checklist.__dict__,
                status = status.HTTP_200_OK
            )
        else:
            return CustomResponse(
                message = f"DailyChecklist with id {daily_checklist_id} does not exist",
                status = status.HTTP_400_BAD_REQUEST
            )
    except Exception as ex:
        return HTTPException(detail="Something went wrong", status_code=status.HTTP_410_GONE)

def update_daily_checklist(db: Session, daily_checklist_data: DailyChecklistUpdate):
    try:
        daily_checklist_in_db = db.query(DailyChecklist).where(DailyChecklist.id == daily_checklist_data.id).first()
        if daily_checklist_in_db is None:
            return CustomResponse(
                message = "Failed",
                exception = f"DailyChecklist with id {daily_checklist_data.id} does not exist",
                status = status.HTTP_400_BAD_REQUEST
            )
        update_fields = daily_checklist_data.dict()
        for field in update_fields.keys():
            setattr(daily_checklist_in_db, field, getattr(daily_checklist_data, field))
        db.commit()
        db.refresh(daily_checklist_in_db)
        response = CustomResponse(
            message = "Successfully",
            data = daily_checklist_in_db.__dict__,
            status = status.HTTP_201_CREATED
        )
        return response
    except exc.IntegrityError:
        return CustomResponse(
            message = "Failed",
            status = status.HTTP_404_NOT_FOUND,
            exception = f"DailyChecklist with name {daily_checklist_data.name} already existed"
        )
    except Exception as ex:
        return HTTPException(detail="Something went wrong", status_code=status.HTTP_410_GONE)


def create_daily_checklist(db: Session, daily_checklist_data: DailyChecklistCreate):
    try:
        daily_checklist_item = DailyChecklist()
        create_fields = list(DailyChecklistCreate.__fields__.keys())
        for field in create_fields:
            setattr(daily_checklist_item, field, getattr(daily_checklist_data, field))
        db.add(daily_checklist_item)
        db.commit()
        db.refresh(daily_checklist_item)
        response = CustomResponse(
            message = "Successfully",
            data = daily_checklist_item.__dict__,
            status = status.HTTP_200_OK
        )
        return response
    except exc.IntegrityError:
        response = CustomResponse(
            message = "Failed",
            status = status.HTTP_404_NOT_FOUND,
            exception = f"daily_checklist with name {daily_checklist_data.name} already exist"
        )
        return response
    except Exception as ex:
        return HTTPException(detail="Something went wrong", status_code=status.HTTP_410_GONE)

def delete_daily_checklist(db: Session, daily_checklist_id: int):
    try:
        daily_checklist_query = db.query(DailyChecklist).where(DailyChecklist.id == daily_checklist_id).first()
        if daily_checklist_query is None:
            return CustomResponse(
                message = "Failed",
                status = status.HTTP_404_NOT_FOUND,
                exception = f"daily_checklist with id {daily_checklist_id} does not exist"
            )
        db.delete(daily_checklist_query)
        db.commit()
        return CustomResponse(
                message = "Succesfully",
                status = status.HTTP_200_OK,
            )
    except Exception as ex:
        return HTTPException(detail="Something went wrong", status_code=status.HTTP_410_GONE)
        
    
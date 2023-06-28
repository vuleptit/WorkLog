from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy import exc
from model.setting import *
from business_rules.view_models.setting_dto import *
from api.utils.custom_response import CustomResponse
from fastapi import status

def get_all_settings(db: Session):
    settings = db.query(Setting).all()
    message = "Successful"
    response = CustomResponse(
        message=message,
        data=settings,
        status=status.HTTP_200_OK
    )
    return response

def get_setting_by_id(db: Session, setting_id: int):
    try:
        setting= db.query(Setting).where(Setting.id == setting_id).first()
    
        if setting is not None:
            return CustomResponse(
                message = "Successfully",
                data = setting.__dict__,
                status = status.HTTP_200_OK
            )
        else:
            return CustomResponse(
                message = f"Setting with id {setting_id} does not exist",
                status = status.HTTP_400_BAD_REQUEST
            )
    except Exception as ex:
        return HTTPException(detail="Something went wrong", status_code=status.HTTP_410_GONE)

def update_setting(db: Session, setting_data: SettingUpdate):
    try:
        setting_in_db = db.query(Setting).where(Setting.id == setting_data.id).first()
        if setting_in_db is None:
            return CustomResponse(
                message = "Failed",
                exception = f"Setting with id {setting_data.id} does not exist",
                status = status.HTTP_400_BAD_REQUEST
            )
        update_fields = setting_data.dict()
        for field in update_fields.keys():
            setattr(setting_in_db, field, getattr(setting_data, field))
        db.commit()
        db.refresh(setting_in_db)
        response = CustomResponse(
            message = "Successfully",
            data = setting_in_db.__dict__,
            status = status.HTTP_201_CREATED
        )
        return response
    except exc.IntegrityError:
        return CustomResponse(
            message = "Failed",
            status = status.HTTP_404_NOT_FOUND,
            exception = f"Setting with name {setting_data.name} already existed"
        )
    except Exception as ex:
        return HTTPException(detail="Something went wrong", status_code=status.HTTP_410_GONE)


def create_setting(db: Session, setting_data: SettingCreate):
    try:
        setting_item = Setting()
        create_fields = list(SettingCreate.__fields__.keys())
        for field in create_fields:
            setattr(setting_item, field, getattr(setting_data, field))
        db.add(setting_item)
        db.commit()
        db.refresh(setting_item)
        response = CustomResponse(
            message = "Successfully",
            data = setting_item.__dict__,
            status = status.HTTP_200_OK
        )
        return response
    except exc.IntegrityError:
        response = CustomResponse(
            message = "Failed",
            status = status.HTTP_404_NOT_FOUND,
            exception = f"setting with name {setting_data.name} already exist"
        )
        return response
    except Exception as ex:
        return HTTPException(detail="Something went wrong", status_code=status.HTTP_410_GONE)

def delete_setting(db: Session, setting_id: int):
    try:
        setting_query = db.query(Setting).where(Setting.id == setting_id).first()
        if setting_query is None:
            return CustomResponse(
                message = "Failed",
                status = status.HTTP_404_NOT_FOUND,
                exception = f"setting with id {setting_id} does not exist"
            )
        db.delete(setting_query)
        db.commit()
        return CustomResponse(
                message = "Succesfully",
                status = status.HTTP_200_OK,
            )
    except Exception as ex:
        return HTTPException(detail="Something went wrong", status_code=status.HTTP_410_GONE)
        
    
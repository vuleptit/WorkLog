from sqlalchemy.orm import Session
from sqlalchemy import exc
from model.user import *
from business_rules.view_models.user_dto import *
from api.utils.custom_response import ResponseModel
from fastapi import status

def get_user_by_id(db: Session, user_id: int):
    try:
        user_query = db.query(User).where(User.id == user_id).first()
        user = user_query.__dict__
        message = "Get user successfully"
        response = ResponseModel(
            message = message,
            data = user,
            status = status.HTTP_200_OK
        )
        return response
    except Exception as ex:
        message = "Get user failed"
        exception = "User with given id does not exist"
        response = ResponseModel(
            message = message,
            status = status.HTTP_404_NOT_FOUND,
            exception = exception
        )
        return response
        

def update_user(db: Session, user_data: UserUpdate):
    try:
        user_in_db = db.query(User).where(User.id == user_data.id).first()
        if user_in_db is not None:
            update_fields = ["email", "password", "phone", "user_name", "is_active"]
            for field in update_fields:
                setattr(user_in_db, field, getattr(user_data, field))
        else:
            raise UserDoesNotExist
        db.commit()
        db.refresh(user_in_db)
        user = user_in_db.__dict__
        message = "Udpate user successfully"
        response = ResponseModel(
            message = message,
            data = user,
            status = status.HTTP_200_OK
        )
        return response
    except exc.SQLAlchemyError:
        message = "Update user failed"
        exception = f"User with email {user_data.email} already exist"
        response = ResponseModel(
            message = message,
            status = status.HTTP_404_NOT_FOUND,
            exception = exception
        )
        return response
    except Exception as UserDoesNotExist:
        message = "Update user failed"
        exception = f"User with given id {user_data.id} does not exist"
        response = ResponseModel(
            message = message,
            status = status.HTTP_404_NOT_FOUND,
            exception = exception
        )
        return response 
        
def create_user(db: Session, user_data: UserCreate):
    try:
        user_item = User()
        create_fields = ["email", "password", "phone", "user_name", "is_active", "is_admin"]
        for field in create_fields:
            setattr(user_item, field, getattr(user_data, field))
        db.add(user_item)
        db.commit()
        db.refresh(user_item)
        user = user_item.__dict__
        message = "Create user successfully"
        response = ResponseModel(
            message = message,
            data = user,
            status = status.HTTP_200_OK
        )
        return response
    except Exception as ex:
        message = "Create user failed"
        exception = f"User with email {user_data.email} already exist"
        response = ResponseModel(
            message = message,
            status = status.HTTP_404_NOT_FOUND,
            exception = exception
        )
        return response
        

def delete_user(db: Session, user_id: int):
    try:
        user_query = db.query(User).where(User.id == user_id).first()
        db.delete(user_query)
        db.commit()
        user_in_db = get_user_by_id(db=db, user_id=user_id)
        message = "Delete user successfully"
        response = ResponseModel(
                message = message,
                status = status.HTTP_200_OK
        )
        return user_in_db
    except Exception as ex:
        message = "Deleted user failed"
        exception = f"User id {user_id} does not exist"
        response = ResponseModel(
            message = message,
            status = status.HTTP_404_NOT_FOUND,
            exception = exception
        )
        return response
        
    
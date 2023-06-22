from sqlalchemy.orm import Session
from sqlalchemy import exc
from model.user import *
from business_rules.view_models.user_dto import *
from api.utils.custom_response import CustomResponse
from fastapi import status
from .jwt_services import get_password_hash
from fastapi import status, Form

def get_all_users(db: Session):
    users = db.query(User).all()
    message = "Get users successfully"
    response = CustomResponse(
        message=message,
        data=users,
        status=status.HTTP_200_OK
    )
    return response

def get_user_by_id(db: Session, user_id: int):
    try:
        user_query = db.query(User).where(User.id == user_id).first()
        user = user_query
        message = "Get user successfully"
        response = CustomResponse(
            message = message,
            data = user,
            status = status.HTTP_200_OK
        )
        return response
    except Exception as ex:
        message = "Get user failed"
        exception = "User with given id does not exist"
        response = CustomResponse(
            message = message,
            status = status.HTTP_404_NOT_FOUND,
            exception = exception
        )
        return response

def update_user(db: Session, user_data: UserUpdate):
    try:
        user_in_db = db.query(User).where(User.id == user_data.id).first()
        print(user_in_db)
        if user_in_db is not None:
            update_fields = user_data.dict()
            update_fields.pop('id')
            for field in update_fields.keys():
                setattr(user_in_db, field, getattr(user_data, field))
        else:
            raise UserDoesNotExist
        db.commit() 
        db.refresh(user_in_db)
        user = user_in_db.__dict__
        message = "Udpate user successfully"
        response = CustomResponse(
            message = message,
            data = user,
            status = status.HTTP_201_CREATED
        )
        return response
    except exc.SQLAlchemyError:
        message = "Update user failed"
        exception = f"User with email {user_data.email} already exist"
        response = CustomResponse(
            message = message,
            status = status.HTTP_404_NOT_FOUND,
            exception = exception
        )
        return response
    except Exception as UserDoesNotExist:
        message = "Update user failed"
        exception = f"User with given id {user_data.id} does not exist"
        response = CustomResponse(
            message = message,
            status = status.HTTP_404_NOT_FOUND,
            exception = exception
        )
        return response

def create_user(db: Session, user_data: UserInDB):
    try:
        user_item = User()
        create_fields = ["email", "phone", "user_name", "is_active", "is_admin"]
        for field in create_fields:
            setattr(user_item, field, getattr(user_data, field))
        user_item.password = get_password_hash(user_data.password)
        db.add(user_item)
        db.commit()
        db.refresh(user_item)
        user = user_item.__dict__
        message = "Create user successfully"
        response = CustomResponse(
            message = message,
            data = user,
            status = status.HTTP_200_OK
        )
        return response
    except Exception as ex:
        message = "Create user failed"
        exception = f"User with email {user_data.email} already exist"
        response = CustomResponse(
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
        if user_in_db.data is None:
            message = "Delete user successfully"
            response = CustomResponse(
                    message = message,
                    status = status.HTTP_200_OK
            )
            return response
        else:
            raise DeleteUserException
    except Exception as DeleteUserException:
        message = "Deleted user failed"
        exception = f"User id {user_id} does not exist"
        response = CustomResponse(
            message = message,
            status = status.HTTP_404_NOT_FOUND,
            exception = exception
        )
        return response
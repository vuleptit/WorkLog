from sqlalchemy.orm import Session

from model.user import *
from business_rules.view_models.user_dto import *

def get_user_by_id(db: Session, user_id: int):
    user_query = db.query(User).where(User.id == user_id).first()
    print(user_query.__dict__)
    user = user_query.__dict__
    # user = {key: value for key, value in user_query.__dict__.items() if not key.startswith('_')}
    return user

def create_or_update_user(db: Session, user_data: UserCreate):
    if user_data.id <= 0:
        # Create new User
        user_item = User()
        user_item.email = user_data.email
        user_item.password = user_data.password
        user_item.phone = user_data.phone
        user_item.user_name = user_data.user_name
        user_item.is_active = user_data.is_active
        user_item.is_admin = user_data.is_admin

        db.add(user_item)
        db.commit()
        db.refresh(user_item)
        return user_item
    else:
        # Update
        user_in_db = get_user_by_id(db=db, user_id=user_data.id)
        user_in_db.email = user_data.email
        user_in_db.password = user_data.password
        user_in_db.phone = user_data.phone
        user_in_db.user_name = user_data.user_name
        user_in_db.is_active = user_data.is_active
        user_in_db.is_admin = user_data.is_admin
        db.commit()
        db.refresh(user_in_db)
        print(type(user_in_db))
        print(user_in_db)
        return user_in_db

def delete_user(db: Session, user_id: int):
    user_query = db.query(User).where(User.id == user_id).first()
    db.delete(user_query)
    db.commit()
    user_in_db = get_user_by_id(db=db, user_id=user_id)
    return user_in_db
    
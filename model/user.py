from database_settings import Base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

class User(Base):
    __tablename__ = 'users'

    email = Column(String, unique=True)
    password = Column(String)
    user_name = Column(String)
    phone = Column(String)
    is_admin = Column(Boolean)
    is_active = Column(Boolean, default=True)
    
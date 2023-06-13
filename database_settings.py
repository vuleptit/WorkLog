import os
from sqlalchemy import create_engine, Integer, Boolean, Column, MetaData, DateTime, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, as_declarative, declared_attr, relationship

user_name = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
SQLALCHEMY_DATABASE_URL = f'postgresql://{user_name}:{password}@postgresserver/db'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@as_declarative()
class Base(object):
    metadata: MetaData

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True, index=True)
    created_date = Column(DateTime, server_default=func.now())
    modified_by = Column(Integer, ForeignKey('users.id'))
    modified_date =  Column(DateTime, server_default=func.now())
    created_by = Column(Integer, ForeignKey('users.id'))

    



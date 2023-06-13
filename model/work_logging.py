from database_settings import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP

class WorkLogging(Base):
    __tablename__ = 'work_logging'
    
    id = Column(Integer, primary_key=True, index=True)
    task_id =  Column(Integer, ForeignKey('task.id'))
    # user = relationship('users')
    time_spent = Column(TIMESTAMP)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_date = Column(TIMESTAMP)
    created_by = Column(Integer)

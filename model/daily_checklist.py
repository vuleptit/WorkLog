from database_settings import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Numeric
from sqlalchemy.types import DateTime

class DailyChecklist(Base):
    __tablename__ = 'daily_checklist'
    
    name = Column(String, unique=True)
    parent_checklist_id = Column(Integer)
    user_id =  Column(Integer, ForeignKey('users.id'))
    is_completed = Column(Boolean)
    estimation_time = Column(Numeric(19, 2))
    task_id = Column(Integer, ForeignKey('task.id'))
    time_estimated = Column(Numeric(19, 2))
    

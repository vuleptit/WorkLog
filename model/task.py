from database_settings import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

class Task(Base):
    __tablename__ = 'task'
    
    name = Column(String, unique=True)
    project_id = Column(Integer, ForeignKey('project.id'))
    code_on_jira = Column(String)

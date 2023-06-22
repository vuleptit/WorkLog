from database_settings import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

class Project(Base):
    __tablename__ = 'project'
    name = Column(String, unique=True)
    code_on_jira = Column(String)

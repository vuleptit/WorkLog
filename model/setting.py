from database_settings import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

class Setting(Base):
    __tablename__ = 'setting'
    
    user_id =  Column(Integer, ForeignKey('users.id'))
    # user = relationship('users')
    email_sending_active = Column(Boolean)
    sms_sending_active = Column(Boolean)
    jira_account = Column(Integer)
    jira_password = Column(Integer)
    jira_base_url = Column(Integer)

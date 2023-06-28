from typing import Union

from pydantic import BaseModel

class SettingCreate(BaseModel):
    user_id: int
    email_sending_active: bool
    sms_sending_active: bool
    jira_account: int
    jira_password: int
    jira_base_url: int

    class Config:
        orm_mode = True
        
class SettingUpdate(BaseModel):
    id: int
    user_id: int
    email_sending_active: bool
    sms_sending_active: bool
    jira_account: int
    jira_password: int
    jira_base_url: int

    class Config:
        orm_mode = True
        

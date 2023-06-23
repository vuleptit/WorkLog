from datetime import datetime
from pydantic import BaseModel

class WorkLoggingCreate(BaseModel):
    task_id: int
    time_spent: datetime
    user_id: int
    
    class Config:
        orm_mode = True
        
class WorkLoggingUpdate(BaseModel):
    id: int
    task_id: int
    time_spent: datetime
    user_id: int

    class Config:
        orm_mode = True
        

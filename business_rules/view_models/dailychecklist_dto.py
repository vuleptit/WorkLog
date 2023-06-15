from typing import Union

from pydantic import BaseModel
from sqlalchemy import Numeric
from decimal import Decimal
class DailyChecklistBase(BaseModel):
    id: int
    name: str
    parent_checklist_id: Union[str, None] = None
    user_id: Union[int, None] = None
    is_completed: bool = False
    estimation_time: Union[Decimal, None] = None
    task_id: Union[int, None] = None
    time_estimated: Union[Decimal, None] = None
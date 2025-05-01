from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TableBase(BaseModel):
    name: str
    capacity: int
    note: Optional[str] = None
    is_active: Optional[bool] = True
    sort_order: Optional[int] = None

class TableCreate(TableBase):
    pass

class TableUpdate(BaseModel):
    name: Optional[str]
    capacity: Optional[int]
    note: Optional[str]
    is_active: Optional[bool]
    sort_order: Optional[int] = None

class TableResponse(TableBase):
    pass
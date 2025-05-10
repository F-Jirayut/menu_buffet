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

class TableUpdate(TableBase):
    pass

class TableResponse(TableBase):
    id: int
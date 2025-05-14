from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class TableBase(BaseModel):
    name: str
    capacity: int
    note: Optional[str] = None
    is_active: Optional[bool] = True
    sort_order: Optional[int] = None
    
    model_config = ConfigDict(
        extra='ignore',
        populate_by_name=True,
        str_strip_whitespace=True,
        from_attributes=True,
        exclude_none=True
    )

class TableCreate(TableBase):
    pass

class TableUpdate(TableBase):
    pass

class TableResponse(TableBase):
    id: int
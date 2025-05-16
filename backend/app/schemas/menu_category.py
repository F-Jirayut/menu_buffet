from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class MenuCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    sort_order: Optional[int] = None
    
    model_config = ConfigDict(
        extra='ignore',
        populate_by_name=True,
        str_strip_whitespace=True,
        from_attributes=True,
        exclude_none=True
    )

class MenuCategoryCreate(MenuCategoryBase):
    pass

class MenuCategoryUpdate(MenuCategoryBase):
    sort_order: int

class MenuCategory(MenuCategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

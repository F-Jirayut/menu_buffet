from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MenuCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None
    sort_order: Optional[int] = None

class MenuCategoryCreate(MenuCategoryBase):
    pass

class MenuCategoryUpdate(MenuCategoryBase):
    sort_order: int

class MenuCategory(MenuCategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

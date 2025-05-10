from pydantic import BaseModel, Field
from typing import Optional

class MenuBase(BaseModel):
    name: str = Field(..., example="ข้าวผัดกะเพรา")
    description: Optional[str] = None
    category_id: int = Field(..., example=1)
    is_available: bool = Field(default=True)
    sort_order: Optional[int] = None

class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    sort_order: int
    pass

class MenuResponse(MenuBase):
    id: int
    image_url: Optional[str] = None

    class Config:
        from_attributes = True 

class MenuInDB(MenuBase):
    id: int
    image_disk: Optional[str] = None
    image_path: Optional[str] = None

    class Config:
        from_attributes = True

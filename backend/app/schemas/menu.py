from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class MenuBase(BaseModel):
    name: str = Field(..., example="ข้าวผัดกะเพรา")
    description: Optional[str] = None
    category_id: int = Field(..., example=1)
    is_available: bool = Field(default=True)
    sort_order: Optional[int] = None
    
    model_config = ConfigDict(
        extra='ignore',
        populate_by_name=True,
        str_strip_whitespace=True,
        from_attributes=True,
        exclude_none=True
    )

class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    sort_order: int
    pass

class MenuResponse(MenuBase):
    id: int
    image_url: Optional[str] = None

class MenuInDB(MenuBase):
    id: int
    image_disk: Optional[str] = None
    image_path: Optional[str] = None

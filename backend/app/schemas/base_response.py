from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.pagination import Pagination

T = TypeVar("T")

class BaseResponse(BaseModel, Generic[T]):
    success: bool
    message: Optional[str] = None
    data: Optional[T] = None
    pagination: Optional[Pagination] = None
    
    model_config = ConfigDict(
        extra='ignore',
        populate_by_name=True,
        str_strip_whitespace=True,
        from_attributes=True,
        exclude_none=True
    )

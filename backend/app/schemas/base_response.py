from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, Field
from app.schemas.pagination import Pagination

T = TypeVar("T")

class BaseResponse(BaseModel, Generic[T]):
    success: bool
    message: Optional[str] = None
    data: Optional[T] = None
    pagination: Optional[Pagination] = None

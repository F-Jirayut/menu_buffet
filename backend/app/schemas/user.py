from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from app.schemas.role import Role

class UserBase(BaseModel):
    name: str
    username: str
    
    model_config = ConfigDict(
        extra='ignore',
        populate_by_name=True,
        str_strip_whitespace=True,
        from_attributes=True,
        exclude_none=True
    )

class UserCreate(UserBase):
    password: Optional[str] = None
    role_id: int

class User(UserBase):
    id: int
    role: Role  # Full object (response)
    created_at: datetime
    updated_at: datetime

class UserLogin(BaseModel):
    username: str
    password: str


class UserProfile(BaseModel):
    id: int
    name: str
    username: str
    role_id: int
    role_name: str
    created_at: datetime
    updated_at: datetime
    permissions: Optional[List] = None
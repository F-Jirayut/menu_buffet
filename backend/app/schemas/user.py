from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.schemas.role import Role

class UserBase(BaseModel):
    name: str
    username: str

class UserCreate(UserBase):
    password: Optional[str] = None
    role_id: int

class User(UserBase):
    id: int
    role: Role  # Full object (response)
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

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
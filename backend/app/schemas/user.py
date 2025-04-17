from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.schemas.role import Role  # ใช้ใน response

class UserBase(BaseModel):
    name: str
    username: str

class UserCreate(UserBase):
    password: str
    role_id: int

class User(UserBase):
    id: int
    role: Role  # Full object (response)
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str

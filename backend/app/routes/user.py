from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.controllers import user_controller
from app.schemas.user import UserCreate, User
from app.database import Database
from app.dependencies.auth import get_current_user
from app.schemas.base_response import BaseResponse
from typing import List
from app.dependencies.user_permission import check_permissions
import re

db_instance = Database()
get_db = db_instance.get_db
prefix = "/users"

resource_permissions = {
    "GET": [
        {"pattern": re.compile(f"^{prefix}/$"), "permissions": ["User.View"]},
        {"pattern": re.compile(f"^{prefix}/[^/]+$"), "permissions": ["User.View"]},
    ],
    "POST": [
        {"pattern": re.compile(f"^{prefix}/$"), "permissions": ["User.Create"]}
    ],
    "PUT": [
        {"pattern": re.compile(f"^{prefix}/[^/]+$"), "permissions": ["User.Update"]}
    ],
    "DELETE": [
        {"pattern": re.compile(f"^{prefix}/[^/]+$"), "permissions": ["User.Delete"]}
    ]
}

router = APIRouter(
    prefix=prefix,
    tags=["Users"],
    dependencies=[
        Depends(get_current_user),
        Depends(check_permissions(resource_permissions, get_db))
    ]
)

@router.post("/", response_model=BaseResponse[User])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_controller.create_user(db=db, user=user)
    return BaseResponse(
        success=True,
        message="User created successfully",
        data=db_user
    )

@router.get("/{user_id}", response_model=BaseResponse[User])
def user(user_id: int, db: Session = Depends(get_db)):
    db_user =  user_controller.get_user_by_id(db, id=user_id)
    return BaseResponse(
        success=True,
        message="User fetched successfully",
        data=db_user
    )

@router.get("/", response_model=BaseResponse[List[User]])
def get_all_users(db: Session = Depends(get_db)):
    db_users = user_controller.get_users(db)
    return BaseResponse(
        success=True,
        message="Users fetched successfully",
        data=db_users
    )

@router.put("/{user_id}", response_model=BaseResponse[User])
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_controller.update_user(db=db, user_id=user_id, user=user)
    return BaseResponse(
        success=True,
        message="User updated successfully",
        data=db_user
    )

@router.delete("/{user_id}", response_model=BaseResponse)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_controller.delete_user(db=db, user_id=user_id)
    return BaseResponse(
        success=True,
        message="User deleted successfully",
        data=None
    )

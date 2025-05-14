from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.controllers import user_controller
from app.schemas.user import UserCreate, User
from app.models import User as ModelUser
from app.database import Database
from app.dependencies.auth import get_current_user
from app.schemas.base_response import BaseResponse
from typing import List, Optional
from app.dependencies.user_permission import check_permissions
import re
from app.utils.query_utils import get_pagination_items, count_pagination_items
from app.schemas.pagination import Pagination

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

@router.post("/", response_model=BaseResponse[User], response_model_exclude_none=True)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_controller.create_user(db=db, user=user)
    return BaseResponse(
        success=True,
        message="User created successfully",
        data=db_user
    )

@router.get("/{user_id}", response_model=BaseResponse[User], response_model_exclude_none=True)
def user(user_id: int, db: Session = Depends(get_db)):
    db_user =  user_controller.get_user_by_id(db, id=user_id)
    return BaseResponse(
        success=True,
        message="User fetched successfully",
        data=db_user
    )

@router.get("/", response_model=BaseResponse[List[User]], response_model_exclude_none=True)
def get_all_users(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None)
):
    skip = (page - 1) * page_size
    db_users = get_pagination_items(
        db=db,
        model=ModelUser,
        skip=skip,
        limit=page_size,
        search=search,
        search_fields=["id", "name"]
    )
    
    total = count_pagination_items(
        db=db,
        model=ModelUser,
        search=search,
        search_fields=["id", "name"]
    )
    
    pages = (total + page_size - 1) // page_size

    return BaseResponse(
        success=True,
        message="Users fetched successfully",
        data=db_users,
        pagination=Pagination(
            page=page,
            page_size=page_size,
            total=total,
            pages=pages
        )
    )

@router.put("/{user_id}", response_model=BaseResponse[User], response_model_exclude_none=True)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_controller.update_user(db=db, user_id=user_id, user=user)
    return BaseResponse(
        success=True,
        message="User updated successfully",
        data=db_user
    )

@router.delete("/{user_id}", response_model=BaseResponse, response_model_exclude_none=True)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user_controller.delete_user(db=db, user_id=user_id)
    return BaseResponse(
        success=True,
        message="User deleted successfully",
        data=None
    )

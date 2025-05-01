from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.controllers import role_controller
from app.schemas.role import RoleCreate, Role, RoleDeleteResponse
from app.models import Role as ModelRole
from app.schemas.base_response import BaseResponse
from app.schemas.pagination import Pagination
from app.database import Database
from app.dependencies.auth import get_current_user
from pydantic import BaseModel
from typing import List, Optional, Dict, Union
from app.dependencies.user_permission import check_permissions
import re
from app.utils.query_utils import get_pagination_items, count_pagination_items

db_instance = Database()
get_db = db_instance.get_db
prefix = "/roles"

resource_permissions = {
    "GET": [
        {"pattern": re.compile(f"^{prefix}/$"), "permissions": ["Role.View"]},
        {"pattern": re.compile(f"^{prefix}/[^/]+$"), "permissions": ["Role.View"]},
    ],
    "POST": [
        {"pattern": re.compile(f"^{prefix}/$"), "permissions": ["Role.Create"]}
    ],
    "PUT": [
        {"pattern": re.compile(f"^{prefix}/[^/]+$"), "permissions": ["Role.Update"]}
    ],
    "DELETE": [
        {"pattern": re.compile(f"^{prefix}/[^/]+$"), "permissions": ["Role.Delete"]}
    ]
}

router = APIRouter(
    prefix=prefix,
    tags=["Roles"],
    dependencies=[
        Depends(get_current_user),
        Depends(check_permissions(resource_permissions, get_db))
    ]
)

@router.post("/", response_model=BaseResponse[Role])
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    db_role = role_controller.create_role(db=db, role=role)
    return BaseResponse(
        success=True,
        message="Role created successfully",
        data=db_role
    )

@router.get("/{role_id}", response_model=BaseResponse[Role])
def role(
    role_id: int,
    include: Optional[str] = Query(None),  # รับ include จาก query
    db: Session = Depends(get_db)
):
    db_role = role_controller.get_role_by_id(db, id=role_id, include=include)
    return BaseResponse(
        success=True,
        message="Role fetched successfully",
        data=db_role
    )

@router.get("/", response_model=BaseResponse[List[Role]])
def get_all_roles(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None)
):
    skip = (page - 1) * page_size
    db_roles = get_pagination_items(
        db=db,
        model=ModelRole,
        skip=skip,
        limit=page_size,
        search=search,
        search_fields=["id", "name"]
    )
    
    total = count_pagination_items(
        db=db,
        model=ModelRole,
        search=search,
        search_fields=["id", "name"]
    )
    
    pages = (total + page_size - 1) // page_size

    return BaseResponse(
        success=True,
        message="Roles fetched successfully",
        data=db_roles,
        pagination=Pagination(
            page=page,
            page_size=page_size,
            total=total,
            pages=pages
        )
    )

@router.put("/{role_id}", response_model=BaseResponse[Role])
def update_role(role_id: int, role: RoleCreate, db: Session = Depends(get_db)):
    db_role = role_controller.update_role(db=db, role_id=role_id, role=role)
    return BaseResponse(
        success=True,
        message="Role updated successfully",
        data=db_role
    )

@router.delete("/{role_id}", response_model=BaseResponse)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    role_controller.delete_role(db=db, role_id=role_id)
    return BaseResponse(
        success=True,
        message="Role deleted successfully",
        data=None
    )

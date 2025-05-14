from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.controllers import permission_controller
from app.models import Permission as ModelPermission
from app.schemas.permission import PermissionCreate, Permission, GroupedPermissions
from app.schemas.base_response import BaseResponse
from app.schemas.pagination import Pagination
from app.database import Database
from app.dependencies.auth import get_current_user
from pydantic import BaseModel
from typing import List, Dict, Optional
from app.dependencies.user_permission import check_permissions
import re
from app.utils.query_utils import get_pagination_items, count_pagination_items

db_instance = Database()
get_db = db_instance.get_db
prefix = "/permissions"

resource_permissions = {
    "GET": [
        {"pattern": re.compile(f"^{prefix}/$"), "permissions": ["Permission.View"]},
        {"pattern": re.compile(f"^{prefix}/[^/]+$"), "permissions": ["Permission.View"]},
    ],
    "POST": [
        {"pattern": re.compile(f"^{prefix}/$"), "permissions": ["Permission.Create"]}
    ],
    "PUT": [
        {"pattern": re.compile(f"^{prefix}/[^/]+$"), "permissions": ["Permission.Update"]}
    ],
    "DELETE": [
        {"pattern": re.compile(f"^{prefix}/[^/]+$"), "permissions": ["Permission.Delete"]}
    ]
}

router = APIRouter(
    prefix=prefix,
    tags=["Permissions"],
    dependencies=[
        Depends(get_current_user),
        Depends(check_permissions(resource_permissions, get_db))
    ]
)

@router.post("/", response_model=BaseResponse[Permission], response_model_exclude_none=True)
def create_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
    db_permission = permission_controller.create_permission(db=db, permission=permission)
    return BaseResponse(
        success=True,
        message="Permission created successfully",
        data=db_permission
    )

@router.get("/{permission_id}", response_model=BaseResponse[Permission], response_model_exclude_none=True)
def permission(permission_id: int, db: Session = Depends(get_db)):
    db_permission = permission_controller.get_permission_by_id(db, id=permission_id)
    return BaseResponse(
        success=True,
        message="Permission fetched successfully",
        data=db_permission
    )

@router.get("/", response_model=BaseResponse[List[Permission]], response_model_exclude_none=True)
def get_all_permissions(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None)
):
    skip = (page - 1) * page_size
    db_permissions = get_pagination_items(
        db=db,
        model=ModelPermission,
        skip=skip,
        limit=page_size,
        search=search,
        search_fields=["id", "name"]
    )
    
    total = count_pagination_items(
        db=db,
        model=ModelPermission,
        search=search,
        search_fields=["id", "name"]
    )
    
    pages = (total + page_size - 1) // page_size

    return BaseResponse(
        success=True,
        message="Permissions fetched successfully",
        data=db_permissions,
        pagination=Pagination(
            page=page,
            page_size=page_size,
            total=total,
            pages=pages
        )
    )

@router.get("/groups/list", response_model=BaseResponse[GroupedPermissions], response_model_exclude_none=True)
def get_grouped_permissions(db: Session = Depends(get_db)):
    db_permissions = permission_controller.get_permissions(db)
    grouped_permissions = permission_controller.get_grouped_permissions(db_permissions)

    return BaseResponse(
        success=True,
        message="Grouped permissions fetched successfully",
        data=grouped_permissions
    )

@router.put("/{permission_id}", response_model=BaseResponse[Permission], response_model_exclude_none=True)
def update_permission(permission_id: int, permission: PermissionCreate, db: Session = Depends(get_db)):
    db_permission = permission_controller.update_permission(db=db, permission_id=permission_id, permission=permission)
    return BaseResponse(
        success=True,
        message="Permission updated successfully",
        data=db_permission
    )

@router.delete("/{permission_id}", response_model=BaseResponse, response_model_exclude_none=True)
def delete_permission(permission_id: int, db: Session = Depends(get_db)):
    permission_controller.delete_permission(db=db, permission_id=permission_id)
    return BaseResponse(
        success=True,
        message="Permission deleted successfully",
        data=None
    )

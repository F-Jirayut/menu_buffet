from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from app.controllers import menu_controller
from app.schemas.menu import MenuResponse, MenuCreate, MenuUpdate
from app.models import Menu
from app.schemas.base_response import BaseResponse
from app.schemas.pagination import Pagination
from app.database import Database
from app.dependencies.auth import get_current_user
from app.dependencies.user_permission import check_permissions
from typing import List, Optional
import re
from app.utils.query_utils import get_pagination_items, count_pagination_items

db_instance = Database()
get_db = db_instance.get_db
prefix = "/menus"

resource_permissions = {
    "GET": [
        {"pattern": re.compile(f"^{prefix}/$"), "permissions": ["Menu.View"]},
        {"pattern": re.compile(f"^{prefix}/[^/]+$"), "permissions": ["Menu.View"]},
    ],
    "POST": [
        {"pattern": re.compile(f"^{prefix}/$"), "permissions": ["Menu.Create"]}
    ],
    "PUT": [
        {"pattern": re.compile(f"^{prefix}/[^/]+$"), "permissions": ["Menu.Update"]}
    ],
    "DELETE": [
        {"pattern": re.compile(f"^{prefix}/[^/]+$"), "permissions": ["Menu.Delete"]}
    ]
}

router = APIRouter(
    prefix=prefix,
    tags=["Menus"],
    dependencies=[
        Depends(get_current_user),
        Depends(check_permissions(resource_permissions, get_db))
    ]
)

@router.post("/", response_model=BaseResponse[MenuResponse], response_model_exclude_none=True)
def create_menu(
    name: str = Form(...),
    description: str = Form(None),
    category_id: int = Form(...),
    is_available: bool = Form(True),
    image: UploadFile = File(None),
    sort_order: Optional[int] = Form(None),
    db: Session = Depends(get_db),
):
    menu_create = MenuCreate(
        name=name,
        description=description,
        category_id=category_id,
        is_available=is_available,
        sort_order=sort_order
    )
    
    db_menu = menu_controller.create_menu(
        db=db,
        menu=menu_create,
        image=image
    )

    return BaseResponse(
        success=True,
        message="Menu created successfully",
        data=db_menu
    )

@router.get("/", response_model=BaseResponse[List[MenuResponse]], response_model_exclude_none=True)
def get_all_menus(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None)
):
    skip = (page - 1) * page_size
    db_menus = get_pagination_items(
        db=db,
        model=Menu,
        skip=skip,
        limit=page_size,
        search=search,
        search_fields=["id", "name"],
        order_by=[
            ("sort_order", False),
            ("id", False),
        ]
    )
    
    total = count_pagination_items(
        db=db,
        model=Menu,
        search=search,
        search_fields=["id", "name"]
    )
    
    pages = (total + page_size - 1) // page_size

    return BaseResponse(
        success=True,
        message="Menus fetched successfully",
        data=db_menus,
        pagination=Pagination(
            page=page,
            page_size=page_size,
            total=total,
            pages=pages
        )
    )

@router.get('/{menu_id}', response_model=BaseResponse[MenuResponse], response_model_exclude_none=True)
def get_menu_by_id(menu_id: int, db: Session = Depends(get_db),  request: Request = None):
    db_menu = menu_controller.get_menu_by_id(
        db=db,
        id=menu_id,
        request=request
    )
    if db_menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    
    return BaseResponse(
        success=True,
        message="Menu fetched successfully",
        data=db_menu
    )

@router.put("/{menu_id}", response_model=BaseResponse[MenuResponse], response_model_exclude_none=True)
def update_menu(
    menu_id: int,
    name: str = Form(...),
    description: str = Form(None),
    category_id: int = Form(...),
    is_available: bool = Form(True),
    image: UploadFile = File(None),
    sort_order: str = Form(...),
    db: Session = Depends(get_db),
):
    menu_update = MenuUpdate(
        name=name,
        description=description,
        category_id=category_id,
        is_available=is_available,
        sort_order=sort_order
    )

    updated_menu = menu_controller.update_menu(
        db=db,
        menu_id=menu_id,
        menu=menu_update,
        image=image
    )

    if not updated_menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    return BaseResponse(
        success=True,
        message="Menu updated successfully",
        data=updated_menu
    )


@router.delete("/{menu_id}", response_model=BaseResponse, response_model_exclude_none=True)
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    menu_controller.delete_menu(db=db,menu_id=menu_id)
    return BaseResponse(
        success=True,
        message="Menu deleted successfully",
        data=None
    )

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.controllers import menu_category_controller
from app.schemas.menu_category import MenuCategoryCreate, MenuCategory, MenuCategoryUpdate
from app.models import MenuCategory as ModelMenuCategory
from app.schemas.pagination import Pagination
from app.database import Database
from app.dependencies.auth import get_current_user
from app.dependencies.user_permission import check_permissions
from app.schemas.base_response import BaseResponse
from typing import List, Optional
import re
from app.utils.query_utils import get_pagination_items, count_pagination_items

db_instance = Database()
get_db = db_instance.get_db
prefix = "/menu_categories"

resource_permissions = {
    "GET": [
        {"pattern": re.compile(f"^{prefix}/$"), "permissions": ["Category.View"]},
        {"pattern": re.compile(f"^{prefix}/[^/]+$"), "permissions": ["Category.View"]},
    ],
    "POST": [
        {"pattern": re.compile(f"^{prefix}/$"), "permissions": ["Category.Create"]}
    ],
    "PUT": [
        {"pattern": re.compile(f"^{prefix}/[^/]+$"), "permissions": ["Category.Update"]}
    ],
    "DELETE": [
        {"pattern": re.compile(f"^{prefix}/[^/]+$"), "permissions": ["Category.Delete"]}
    ]
}

router = APIRouter(
    prefix=prefix,
    tags=["Menu_Categories"],
    dependencies=[
        Depends(get_current_user),
        Depends(check_permissions(resource_permissions, get_db))
    ]
)

@router.post("/", response_model=BaseResponse[MenuCategory], response_model_exclude_none=True)
def create_menu_category(menu_category: MenuCategoryCreate, db: Session = Depends(get_db)):
    db_menu_category = menu_category_controller.create_menu_category(db=db, menu_category=menu_category)
    return BaseResponse(
        success=True,
        message="Menu category created successfully",
        data=db_menu_category
    )

@router.get("/{menu_category_id}", response_model=BaseResponse[MenuCategory], response_model_exclude_none=True)
def menu_category(menu_category_id: int, db: Session = Depends(get_db)):
    db_menu_category =  menu_category_controller.get_menu_category_by_id(db, id=menu_category_id)
    return BaseResponse(
        success=True,
        message="Menu category fetched successfully",
        data=db_menu_category
    )

@router.get("/", response_model=BaseResponse[List[MenuCategory]], response_model_exclude_none=True)
def get_all_menu_categories(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None)
):
    skip = (page - 1) * page_size
    db_menus = get_pagination_items(
        db=db,
        model=ModelMenuCategory,
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
        model=ModelMenuCategory,
        search=search,
        search_fields=["id", "name"]
    )
    
    pages = (total + page_size - 1) // page_size

    return BaseResponse(
        success=True,
        message="Menu categories fetched successfully",
        data=db_menus,
        pagination=Pagination(
            page=page,
            page_size=page_size,
            total=total,
            pages=pages
        )
    )

@router.put("/{menu_category_id}", response_model=BaseResponse[MenuCategory], response_model_exclude_none=True)
def update_menu_category(menu_category_id: int, menu_category: MenuCategoryUpdate, db: Session = Depends(get_db)):
    db_menu_category = menu_category_controller.update_menu_category(db=db, menu_category_id=menu_category_id, menu_category=menu_category)
    return BaseResponse(
        success=True,
        message="Menu Category updated successfully",
        data=db_menu_category
    )

@router.delete("/{menu_category_id}", response_model=BaseResponse, response_model_exclude_none=True)
def delete_menu_category(menu_category_id: int, db: Session = Depends(get_db)):
    menu_category_controller.delete_menu_category(db=db, menu_category_id=menu_category_id)
    return BaseResponse(
        success=True,
        message="Menu Category deleted successfully",
        data=None
    )

from app.controllers import order_item_controller
from app.utils.query_utils import count_pagination_items, get_pagination_items, parse_order_by_params
from app.schemas.pagination import Pagination
from app.controllers.controller import paginate_controller
from app.models import OrderItem
from fastapi import APIRouter, Depends, HTTPException,Query, Body
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session, joinedload
from app.schemas.order_item import OrderItemResponse, OrderItemCreate, OrderItemUpdate
from app.schemas.base_response import BaseResponse
from app.database import Database
from app.dependencies.auth import get_current_user
from app.dependencies.user_permission import check_permissions
from typing import List, Optional
import re

db_instance = Database()
get_db = db_instance.get_db
prefix = "/order_items"

resource_permissions = {
    "GET": [
        {"pattern": re.compile(f"^{prefix}/$"), "permissions": ["OrderItem.View"]},
        {"pattern": re.compile(f"^{prefix}/[^/]+$"), "permissions": ["OrderItem.View"]},
    ],
    "POST": [
        {"pattern": re.compile(f"^{prefix}/$"), "permissions": ["OrderItem.Create"]}
    ],
    "PUT": [
        {"pattern": re.compile(f"^{prefix}/[^/]+$"), "permissions": ["OrderItem.Update"]}
    ],
    "DELETE": [
        {"pattern": re.compile(f"^{prefix}/[^/]+$"), "permissions": ["OrderItem.Delete"]}
    ]
}

router = APIRouter(
    prefix=prefix,
    tags=["Order_Items"],
    dependencies=[
        Depends(get_current_user),
        Depends(check_permissions(resource_permissions, get_db))
    ]
)

@router.get("/", response_model=BaseResponse[List[OrderItemResponse]])
def get_orders(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    search_fields: Optional[List[str]] = Query(["id", "name"]),
    order_by: Optional[List[str]] = Query(None)  # เช่น ["name:asc", "created_at:desc"]
):
    items, total, pages = paginate_controller(
        db=db,
        model=OrderItem,
        page=page,
        page_size=page_size,
        search=search,
        order_by=order_by,
        search_fields=search_fields,
        options=[joinedload(OrderItem.menu)]
    )
    
    return BaseResponse(
        success=True,
        message="Order items fetched successfully",
        data=items,
        pagination=Pagination(
            page=page,
            page_size=page_size,
            total=total,
            pages=pages
        )
    )
    
@router.get("/{order_id}", response_model=BaseResponse[OrderItemResponse], response_model_exclude={"pagination"})
def order(
    order_id: int,
    db: Session = Depends(get_db)
):
    db_order = order_item_controller.get_order_item_by_id(db, id=order_id, include_menu=True)
    if not db_order:
        raise HTTPException(status_code=404, detail="Order item not found")
    return BaseResponse(
        success=True,
        message="Order item fetched successfully",
        data=db_order
    )
    
@router.post("/", response_model=BaseResponse[List[OrderItemResponse]], response_model_exclude={"pagination"})
def create_order(order_items: List[OrderItemCreate] = Body(..., min_items=1, max_items=10), db: Session = Depends(get_db)):
    db_order_items = order_item_controller.create_order_item(db=db, order_items=order_items)
    return BaseResponse(
        success=True,
        message="Order item created successfully",
        data=db_order_items
    )
    
@router.put("/", response_model=BaseResponse[List[OrderItemResponse]], response_model_exclude={"pagination"})
def update_orders(
    order_items: List[OrderItemUpdate] = Body(..., min_items=1, max_items=10),
    db: Session = Depends(get_db)
):
    db_orders = order_item_controller.update_order_items(db=db, order_items=order_items)
    return BaseResponse(
        success=True,
        message="Order items updated successfully",
        data=db_orders
    )

# @router.delete("/{order_id}", response_model=BaseResponse, response_model_exclude={"pagination"})
# def delete_order(order_id: int, db: Session = Depends(get_db)):
#     order_item_controller.delete_order(db=db, order_id=order_id)
#     return BaseResponse(
#         success=True,
#         message="Order item deleted successfully",
#         data=None
#     )

from app.controllers import order_controller
from app.utils.query_utils import count_pagination_items, get_pagination_items, parse_order_by_params
from app.schemas.pagination import Pagination
from app.controllers.controller import paginate_controller
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File, Form, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session, joinedload
from app.schemas.order import OrderResponse, OrderCreate, OrderUpdate
from app.schemas.base_response import BaseResponse
from app.database import Database
from app.dependencies.auth import get_current_user
from app.dependencies.user_permission import check_permissions
from typing import List, Optional, Tuple
from app.models import Order
import re

db_instance = Database()
get_db = db_instance.get_db
prefix = "/orders"

resource_permissions = {
    "GET": [
        {"pattern": re.compile(f"^{prefix}/$"), "permissions": ["Order.View"]},
        {"pattern": re.compile(f"^{prefix}/[^/]+$"), "permissions": ["Order.View"]},
    ],
    "POST": [
        {"pattern": re.compile(f"^{prefix}/$"), "permissions": ["Order.Create"]}
    ],
    "PUT": [
        {"pattern": re.compile(f"^{prefix}/[^/]+$"), "permissions": ["Order.Update"]}
    ],
    "DELETE": [
        {"pattern": re.compile(f"^{prefix}/[^/]+$"), "permissions": ["Order.Delete"]}
    ]
}

router = APIRouter(
    prefix=prefix,
    tags=["Orders"],
    dependencies=[
        Depends(get_current_user),
        Depends(check_permissions(resource_permissions, get_db))
    ]
)

@router.get("/", response_model=BaseResponse[List[OrderResponse]], response_model_exclude_none=True)
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
        model=Order,
        page=page,
        page_size=page_size,
        search=search,
        order_by=order_by,
        search_fields=search_fields,
        options=[joinedload(Order.customer)]
    )
    
    return BaseResponse(
        success=True,
        message="Orders fetched successfully",
        data=items,
        pagination=Pagination(
            page=page,
            page_size=page_size,
            total=total,
            pages=pages
        )
    )
    
@router.get("/{order_id}", response_model=BaseResponse[OrderResponse], response_model_exclude_none=True)
def order(
    order_id: int,
    db: Session = Depends(get_db)
):
    db_order = order_controller.get_order_by_id(db, id=order_id)
    return BaseResponse(
        success=True,
        message="Order fetched successfully",
        data=db_order
    )
    
@router.post("/", response_model=BaseResponse[OrderResponse], response_model_exclude_none=True)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = order_controller.create_order(db=db, order=order)
    return BaseResponse(
        success=True,
        message="Order created successfully",
        data=db_order
    )
    
@router.put("/{order_id}", response_model=BaseResponse[OrderResponse], response_model_exclude_none=True)
def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
    db_order = order_controller.update_order(db=db, order_id=order_id, order=order)
    return BaseResponse(
        success=True,
        message="Order updated successfully",
        data=db_order
    )

@router.delete("/{order_id}", response_model=BaseResponse, response_model_exclude_none=True)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order_controller.delete_order(db=db, order_id=order_id)
    return BaseResponse(
        success=True,
        message="Order deleted successfully",
        data=None
    )

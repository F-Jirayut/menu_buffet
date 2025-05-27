from tokenize import group
from app.controllers import order_item_controller
# from app.utils.query_utils import apply_count_to_query, apply_pagination_to_query
# from app.schemas.pagination import Pagination
# from app.controllers.controller import paginate_controller
from app.models import OrderItem
from fastapi import APIRouter, Depends, HTTPException,Query, Body
from sqlalchemy.orm import Session
from sqlalchemy import or_, cast, String, desc, asc
from app.schemas.order_item import GroupedOrderItemResponse, OrderItemResponse, OrderItemCreate, OrderItemUpdate
from app.schemas.base_response import BaseResponse
from app.database import Database
from app.dependencies.auth import get_current_user
from app.dependencies.user_permission import check_permissions
from typing import List, Optional
import re
from datetime import date as lib_date, time, timedelta, datetime
from collections import defaultdict

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

@router.get("/grouped", response_model=BaseResponse[List[GroupedOrderItemResponse]])
def get_orders(
    db: Session = Depends(get_db),
    order_by: Optional[List[str]] = Query(None),
    date: lib_date = Query(default_factory=lib_date.today),
):
    group_order_items = order_item_controller.get_grouped_order_items(
        db=db,
        date=date,
        order_by=order_by
    )

    return BaseResponse(
        success=True,
        message="Order items fetched successfully",
        data=group_order_items,
    )

# @router.get("/", response_model=BaseResponse[List[OrderItemResponse]])
# def get_orders(
#     db: Session = Depends(get_db),
#     page: int = Query(1, ge=1),
#     page_size: int = Query(10, ge=1, le=100),
#     search: Optional[str] = Query(None),
#     search_fields: Optional[List[str]] = Query(["id", "name"]),
#     order_by: Optional[List[str]] = Query(None),
#     date: lib_date = Query(default_factory=lib_date.today),
# ):
#     skip = (page - 1) * page_size

#     start_datetime = datetime.combine(date, time.min)
#     end_datetime = datetime.combine(date, time.max)

#     query = db.query(OrderItem).filter(
#         OrderItem.created_at >= start_datetime,
#         OrderItem.created_at <= end_datetime,
#     )

#     if search:
#         conditions = [
#             getattr(OrderItem, field).ilike(f"%{search}%")
#             for field in search_fields or []
#             if hasattr(OrderItem, field)
#         ]
#         if conditions:
#             query = query.filter(or_(*conditions))

#     if order_by:
#         for order in order_by:
#             field, _, direction = order.partition(":")
#             if hasattr(OrderItem, field):
#                 column = getattr(OrderItem, field)
#                 query = query.order_by(desc(column) if direction == "desc" else asc(column))
#     else:
#         query = query.order_by(OrderItem.id.asc())

#     total = apply_count_to_query(query)
#     items = apply_pagination_to_query(query, skip=skip, limit=page_size)
#     pages = (total + page_size - 1) // page_size

#     return BaseResponse(
#         success=True,
#         message="Order items fetched successfully",
#         data=items,
#         pagination=Pagination(
#             page=page,
#             page_size=page_size,
#             total=total,
#             pages=pages
#         )
#     )
    
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

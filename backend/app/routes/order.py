from app.controllers import order_controller
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File, Form, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.schemas.order import OrderResponse, OrderCreate, OrderUpdate
from app.schemas.base_response import BaseResponse
from app.database import Database
from app.dependencies.auth import get_current_user
from app.dependencies.user_permission import check_permissions
from typing import List, Optional
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

@router.get("/", response_model=BaseResponse[List[OrderResponse]])
def get_orders(db: Session = Depends(get_db), search: Optional[str] = Query(None)):
    
    db_order = order_controller.get_orders(db, search)
    return BaseResponse(
        success=True,
        message="Order fetched successfully",
        data=db_order
    )
    
# @router.get("/{order_id}", response_model=BaseResponse[OrderResponse])
# def order(
#     order_id: int,
#     db: Session = Depends(get_db)
# ):
#     db_order = order_controller.get_order_by_id(db, id=order_id)
#     return BaseResponse(
#         success=True,
#         message="Order fetched successfully",
#         data=db_order
#     )
    
# @router.post("/", response_model=BaseResponse[OrderResponse])
# def create_order(order: OrderCreate, db: Session = Depends(get_db)):
#     db_order = order_controller.create_order(db=db, order=order)
#     return BaseResponse(
#         success=True,
#         message="Order created successfully",
#         data=db_order
#     )
    
# @router.put("/{order_id}", response_model=BaseResponse[OrderResponse])
# def update_order(order_id: int, order: OrderUpdate, db: Session = Depends(get_db)):
#     db_order = order_controller.update_order(db=db, order_id=order_id, order=order)
#     return BaseResponse(
#         success=True,
#         message="Order updated successfully",
#         data=db_order
#     )

# @router.delete("/{order_id}", response_model=BaseResponse)
# def delete_order(order_id: int, db: Session = Depends(get_db)):
#     order_controller.delete_order(db=db, order_id=order_id)
#     return BaseResponse(
#         success=True,
#         message="Order deleted successfully",
#         data=None
#     )

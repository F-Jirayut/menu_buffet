from app.controllers import customer_controller
from app.utils.query_utils import count_pagination_items, get_pagination_items, parse_order_by_params
from app.schemas.pagination import Pagination
from app.controllers.controller import paginate_controller
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File, Form, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session, joinedload
from app.schemas.customer import CustomerResponse, CustomerCreate, CustomerUpdate
from app.schemas.base_response import BaseResponse
from app.database import Database
from app.dependencies.auth import get_current_user
from app.dependencies.user_permission import check_permissions
from typing import List, Optional, Tuple
from app.models import Customer
import re

db_instance = Database()
get_db = db_instance.get_db
prefix = "/customers"

resource_permissions = {
    "GET": [
        {"pattern": re.compile(f"^{prefix}/$"), "permissions": ["Customer.View"]},
        {"pattern": re.compile(f"^{prefix}/[^/]+$"), "permissions": ["Customer.View"]},
    ],
    "POST": [
        {"pattern": re.compile(f"^{prefix}/$"), "permissions": ["Customer.Create"]}
    ],
    "PUT": [
        {"pattern": re.compile(f"^{prefix}/[^/]+$"), "permissions": ["Customer.Update"]}
    ],
    "DELETE": [
        {"pattern": re.compile(f"^{prefix}/[^/]+$"), "permissions": ["Customer.Delete"]}
    ]
}

router = APIRouter(
    prefix=prefix,
    tags=["Customers"],
    dependencies=[
        Depends(get_current_user),
        Depends(check_permissions(resource_permissions, get_db))
    ]
)

@router.get("/", response_model=BaseResponse[List[CustomerResponse]], response_model_exclude_none=True)
def get_customers(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None),
    order_by: Optional[List[str]] = Query(None)
):
    items, total, pages = paginate_controller(
        db=db,
        model=Customer,
        page=page,
        page_size=page_size,
        search=search,
        order_by=order_by,
        search_fields=["id", "name", "email", "phone"],
        options=None
    )

    return BaseResponse(
        success=True,
        message="Customers fetched successfully",
        data=items,
        pagination=Pagination(
            page=page,
            page_size=page_size,
            total=total,
            pages=pages
        )
    )
    
@router.get("/{customer_id}", response_model=BaseResponse[CustomerResponse], response_model_exclude_none=True)
def customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    db_customer = customer_controller.get_customer_by_id(db, id=customer_id)
    return BaseResponse(
        success=True,
        message="Customer fetched successfully",
        data=db_customer
    )
    
@router.post("/", response_model=BaseResponse[CustomerResponse], response_model_exclude_none=True)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    db_customer = customer_controller.create_customer(db=db, customer=customer)
    return BaseResponse(
        success=True,
        message="Customer created successfully",
        data=db_customer
    )
    
@router.put("/{customer_id}", response_model=BaseResponse[CustomerResponse], response_model_exclude_none=True)
def update_customer(customer_id: int, customer: CustomerUpdate, db: Session = Depends(get_db)):
    db_customer = customer_controller.update_customer(db=db, customer_id=customer_id, customer=customer)
    return BaseResponse(
        success=True,
        message="Customer updated successfully",
        data=db_customer
    )

@router.delete("/{customer_id}", response_model=BaseResponse, response_model_exclude_none=True)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer_controller.delete_customer(db=db, customer_id=customer_id)
    return BaseResponse(
        success=True,
        message="Customer deleted successfully",
        data=None
    )

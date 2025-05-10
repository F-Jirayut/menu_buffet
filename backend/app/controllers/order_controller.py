

from app.models import Order
from app.schemas.order import OrderCreate, OrderUpdate
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from sqlalchemy import func, or_, cast, String
from typing import Dict, Optional

def get_orders(db: Session, search: Optional[str] = None):
    query = db.query(Order)

    if search:
        search_like = f"%{search}%"
        query = query.filter(
            or_(
                cast(Order.id, String).like(search_like),
                Order.name.like(search_like)
            )
        )

    return query.order_by(Order.sort_order).all()

# def get_order_by_name(db: Session, name: str):
#     return db.query(Order).filter(Order.name == name).first()

# def get_order_by_id(db: Session, id: int):
#     return db.query(Order).filter(Order.id == id).first()

# def create_order(db: Session, order: OrderCreate):
#     existing_order = get_order_by_name(db, order.name)
#     if existing_order:
#         raise HTTPException(status_code=400, detail="Order already exists")

#     sort_order = order.sort_order
#     if order.sort_order is None:
#         max_sort = db.query(func.max(Order.sort_order)).scalar() or 0
#         sort_order = max_sort + 1

#     db_order = Order(
#         name=order.name,
#         capacity=order.capacity,
#         note=order.note,
#         is_active=order.is_active,
#         sort_order=sort_order
#     )
#     db.add(db_order)
    
#     try:
#         db.commit()
#         db.refresh(db_order)
#     except SQLAlchemyError as e:
#         db.rollback()
#         print(str(e))
#         raise HTTPException(status_code=500, detail=f"Error creating order: {str(e)}")

#     return db_order

# def update_order(db: Session, order_id: int, order: OrderUpdate) -> Order:
#     db_order = db.query(Order).filter(Order.id == order_id).first()
#     if not db_order:
#         raise HTTPException(status_code=404, detail="Order not found")
#     try:
#         db_order.name = order.name
#         db_order.capacity = order.capacity
#         db_order.note = order.note
#         db_order.is_active = order.is_active
#         db_order.sort_order = order.sort_order
#         db.commit()
#         db.refresh(db_order)
#     except SQLAlchemyError as e:
#         db.rollback()
#         print(str(e))
#         raise HTTPException(status_code=500, detail="Error updating order")
#     return db_order

# def delete_order(db: Session, order_id: int) -> Dict[str, str]:
#     db_order = db.query(Order).filter(Order.id == order_id).first()
#     if not db_order:
#         raise HTTPException(status_code=404, detail="Order not found")
#     try:
#         db.delete(db_order)
#         db.commit()
#     except SQLAlchemyError as e:
#         db.rollback()
#         print(str(e))
#         raise HTTPException(status_code=500, detail="Error deleting order")
    
#     return {"message": "Order deleted successfully"}
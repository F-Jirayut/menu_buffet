from calendar import c
from app.models import Order, OrderItem, Menu
from app.schemas.order_item import OrderItemCreate, OrderItemUpdate
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from sqlalchemy import func, or_, cast, String, and_
from typing import Dict, Optional, List
from datetime import datetime
import zoneinfo

def get_order_items(db: Session, search: Optional[str] = None):
    query = db.query(OrderItem)

    if search:
        search_like = f"%{search}%"
        query = query.filter(
            or_(
                cast(OrderItem.id, String).like(search_like)
                # OrderItem.menu_name.like(search_like)
            )
        )

    return query.order_by(OrderItem.sort_order).all()

def get_order_item_by_name(db: Session, name: str):
    return db.query(OrderItem).filter(OrderItem.name == name).first()

def get_order_item_by_id(db: Session, id: int, include_menu: bool = False):
    if include_menu:
        return db.query(OrderItem).filter(OrderItem.id == id).options(joinedload(OrderItem.menu)).first()
    return db.query(OrderItem).filter(OrderItem.id == id).first()

def create_order_item(db: Session, order_items: List[OrderItemCreate]):
    if not order_items:
        raise HTTPException(status_code=400, detail="No order items provided")

    now = datetime.now(zoneinfo.ZoneInfo("Asia/Bangkok"))

    db_order = db.query(Order).filter(Order.id == order_items[0].order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    overlap_exists = db.query(Order).filter(
        and_(
            Order.table_id == db_order.table_id,
            Order.status != 'completed',
            Order.started_at <= now,
            Order.ended_at >= now
        )
    ).first()

    if not overlap_exists:
        raise HTTPException(status_code=400, detail="หมดเวลาสั่งอาหารแล้ว")

    db_items = []

    for item in order_items:
        # ตรวจสอบว่า menu_id มีอยู่จริง
        db_menu = db.query(Menu).filter(Menu.id == item.menu_id).first()
        if not db_menu:
            raise HTTPException(status_code=404, detail=f"Menu not found for ID {item.menu_id}")

        db_items.append(OrderItem(
            menu_id=item.menu_id,
            menu_name=db_menu.name,
            order_id=item.order_id,
            quantity=item.quantity,
            price=item.price,
            status=item.status,
            note=item.note,
            created_at=now,
            updated_at=now,
        ))

    try:
        db.add_all(db_items)
        db.commit()
        for item in db_items:
            db.refresh(item)
    except SQLAlchemyError as e:
        db.rollback()
        print(str(e))
        raise HTTPException(status_code=500, detail=f"Error creating order items: {str(e)}")

    return db_items

def update_order_items(db: Session, order_items: List[OrderItemUpdate]):
    updated_items = []

    for item in order_items:
        db_item = db.query(OrderItem).filter(OrderItem.id == item.id).first()
        if not db_item:
            raise HTTPException(status_code=404, detail=f"OrderItem not found: ID {item.id}")
        
        order = db_item.order
        if not order:
            raise HTTPException(status_code=404, detail=f"Order not found for OrderItem ID 1 {item.id}")
        
        now = datetime.now(zoneinfo.ZoneInfo("Asia/Bangkok"))
        overlap_exists = db.query(Order).filter(
            and_(
                Order.table_id == order.table_id,
                Order.status != 'completed',
                Order.started_at <= now,
                Order.ended_at >= now
            )
        ).first()
        
        if not overlap_exists:
            raise HTTPException(status_code=400, detail="หมดเวลาสั่งอาหารแล้ว")

        if item.quantity is not None:
            db_item.quantity = item.quantity

        if item.status is not None: 
            db_item.status = item.status

        if item.note is not None:
            db_item.note = item.note

        updated_items.append(db_item)

    try:
        db.add_all(updated_items)
        db.commit()
        for item in updated_items:
            db.refresh(item)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating order items: {str(e)}")

    return updated_items

# def delete_order(db: Session, order_id: int) -> Dict[str, str]:
#     db_order_item = db.query(OrderItem).filter(OrderItem.id == order_id).first()
#     if not db_order_item:
#         raise HTTPException(status_code=404, detail="Order item not found")
#     try:
#         db.delete(db_order_item)
#         db.commit()
#     except SQLAlchemyError as e:
#         db.rollback()
#         print(str(e))
#         raise HTTPException(status_code=500, detail="Error deleting order item")
    
#     return {"message": "Order item deleted successfully"}
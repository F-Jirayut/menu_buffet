

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
                cast(OrderItem.id, String).like(search_like),
                OrderItem.menu_name.like(search_like)
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

        db_item = OrderItem(
            menu_id=item.menu_id,
            menu_name=item.menu_name,
            order_id=item.order_id,
            quantity=item.quantity,
            price=item.price,
            status=item.status,
            note=item.note,
            created_at=now,
            updated_at=now,
        )
        db.add(db_item)
        db_items.append(db_item)

    try:
        db.commit()
        for item in db_items:
            db.refresh(item)
    except SQLAlchemyError as e:
        db.rollback()
        print(str(e))
        raise HTTPException(status_code=500, detail=f"Error creating order items: {str(e)}")

    return db_items

# def update_order(db: Session, order_id: int, order: OrderUpdate) -> Order:
#     db_order_item = db.query(Order).filter(Order.id == order_id).first()
#     if not db_order_item:
#         raise HTTPException(status_code=404, detail="Order item not found")

#     # ตรวจสอบว่ามีคำสั่งซื้ออื่นที่มีช่วงเวลาทับซ้อนกับคำสั่งซื้อที่อัปเดต (ยกเว้นตัวเอง)
#     overlapping_order = db.query(Order).filter(
#         Order.table_id == order.table_id,  # ตรวจสอบตาม table_id
#         Order.status != 'completed',  # ตรวจสอบว่าไม่ใช่สถานะ 'completed'
#         Order.id != order_id,  # ตรวจสอบว่าไม่ใช่คำสั่งซื้อนี้เอง
#         Order.started_at < order.ended_at,   # started_at ของคำสั่งซื้อใหม่ต้องหลังจาก ended_at ของคำสั่งซื้อเก่า
#         Order.ended_at > order.started_at  # ended_at ของคำสั่งซื้อเก่าต้องหลังจาก started_at ของคำสั่งซื้อใหม่
#     ).first()

#     if overlapping_order:
#         raise HTTPException(status_code=400, detail="มีคำสั่งซื้อที่มีอยู่แล้วและมีระยะเวลาทับซ้อนกัน")

#     # อัปเดตคำสั่งซื้อใหม่ในฐานข้อมูล
#     db_order_item.table_id = order.table_id
#     db_order_item.customer_id = order.customer_id
#     db_order_item.reserved_at = order.reserved_at
#     db_order_item.started_at = order.started_at
#     db_order_item.ended_at = order.ended_at
#     db_order_item.status = order.status
#     db_order_item.total_price = order.total_price
#     db_order_item.note = order.note

#     # บันทึกการอัปเดต
#     try:
#         db.commit()
#         db.refresh(db_order_item)
#     except SQLAlchemyError as e:
#         db.rollback()
#         print(str(e))
#         raise HTTPException(status_code=500, detail="Error updating order item")

#     return db_order_item


def delete_order(db: Session, order_id: int) -> Dict[str, str]:
    db_order_item = db.query(OrderItem).filter(OrderItem.id == order_id).first()
    if not db_order_item:
        raise HTTPException(status_code=404, detail="Order item not found")
    try:
        db.delete(db_order_item)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        print(str(e))
        raise HTTPException(status_code=500, detail="Error deleting order item")
    
    return {"message": "Order item deleted successfully"}
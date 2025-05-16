

from app.models import Order
from app.schemas.order import OrderCreate, OrderUpdate
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from sqlalchemy import func, or_, cast, String
from typing import Dict, Optional
from collections import defaultdict
from datetime import datetime

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

def get_order_by_name(db: Session, name: str):
    return db.query(Order).filter(Order.name == name).first()

def get_order_by_id(
    db: Session,
    id: int,
    include_items: bool = False,
    include_group_order_items: bool = False
):
    query = db.query(Order).filter(Order.id == id)

    # load order_items ด้วย joinedload เฉพาะตอนต้องใช้
    if include_items or include_group_order_items:
        query = query.options(joinedload(Order.order_items))

    order = query.first()

    if not order:
        return None

    # จัดกลุ่ม order_items ถ้าต้องการ
    if include_group_order_items:
        groups = defaultdict(list)
        for item in order.order_items:
            order_date = item.created_at.strftime("%Y-%m-%d %H:%M:%S")
            groups[order_date].append(item)

        # แนบ group_order_items เข้าไปใน object (ทำงานเฉพาะ Pydantic schema ที่รับจาก_attributes)
        order.group_order_items = [
            {
                "created_at": order_date,
                "order_items": items
            }
            for order_date, items in groups.items()
        ]
    else:
        order.group_order_items = []

    # ถ้าไม่ต้องการ order_items → ล้างทิ้งให้ไม่ส่งออก
    if not include_items:
        order.order_items = []
        
    return order

def create_order(db: Session, order: OrderCreate):
    overlapping_order = db.query(Order).filter(
        Order.table_id == order.table_id,  # ตรวจสอบตาม table_id
        Order.status != 'completed',  # ตรวจสอบว่าไม่ใช่สถานะ 'completed'
        Order.started_at < order.ended_at,  # started_at ของคำสั่งซื้อใหม่ต้องหลังจาก ended_at ของคำสั่งซื้อเก่า
        Order.ended_at > order.started_at  # ended_at ต้องหลังจาก started_at ของคำสั่งซื้อใหม่
    ).first()

    if overlapping_order:
        raise HTTPException(status_code=400, detail="มีคำสั่งซื้อที่มีอยู่แล้วและมีระยะเวลาทับซ้อนกัน")
    
    db_order = Order(
        table_id=order.table_id,
        customer_id=order.customer_id,
        reserved_at=order.reserved_at,
        started_at=order.started_at,
        ended_at=order.ended_at,
        status=order.status,
        total_price=order.total_price,
        note=order.note,
    )

    db.add(db_order)

    try:
        db.commit()
        db.refresh(db_order)
    except SQLAlchemyError as e:
        db.rollback()
        print(str(e))
        raise HTTPException(status_code=500, detail=f"Error creating order: {str(e)}")

    return db_order

def update_order(db: Session, order_id: int, order: OrderUpdate) -> Order:
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")

    # ตรวจสอบว่ามีคำสั่งซื้ออื่นที่มีช่วงเวลาทับซ้อนกับคำสั่งซื้อที่อัปเดต (ยกเว้นตัวเอง)
    overlapping_order = db.query(Order).filter(
        Order.table_id == order.table_id,  # ตรวจสอบตาม table_id
        Order.status != 'completed',  # ตรวจสอบว่าไม่ใช่สถานะ 'completed'
        Order.id != order_id,  # ตรวจสอบว่าไม่ใช่คำสั่งซื้อนี้เอง
        Order.started_at < order.ended_at,   # started_at ของคำสั่งซื้อใหม่ต้องหลังจาก ended_at ของคำสั่งซื้อเก่า
        Order.ended_at > order.started_at  # ended_at ของคำสั่งซื้อเก่าต้องหลังจาก started_at ของคำสั่งซื้อใหม่
    ).first()

    if overlapping_order:
        raise HTTPException(status_code=400, detail="มีคำสั่งซื้อที่มีอยู่แล้วและมีระยะเวลาทับซ้อนกัน")

    # อัปเดตคำสั่งซื้อใหม่ในฐานข้อมูล
    db_order.table_id = order.table_id
    db_order.customer_id = order.customer_id
    db_order.reserved_at = order.reserved_at
    db_order.started_at = order.started_at
    db_order.ended_at = order.ended_at
    db_order.status = order.status
    db_order.total_price = order.total_price
    db_order.note = order.note

    # บันทึกการอัปเดต
    try:
        db.commit()
        db.refresh(db_order)
    except SQLAlchemyError as e:
        db.rollback()
        print(str(e))
        raise HTTPException(status_code=500, detail="Error updating order")

    return db_order


def delete_order(db: Session, order_id: int) -> Dict[str, str]:
    db_order = db.query(Order).filter(Order.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    try:
        db.delete(db_order)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        print(str(e))
        raise HTTPException(status_code=500, detail="Error deleting order")
    
    return {"message": "Order deleted successfully"}
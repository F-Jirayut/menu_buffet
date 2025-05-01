

from app.models import Table
from app.schemas.table import TableCreate
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from sqlalchemy import func, or_, cast, String
from typing import Optional

def get_tables(db: Session, search: Optional[str] = None):
    query = db.query(Table)

    if search:
        search_like = f"%{search}%"
        query = query.filter(
            or_(
                cast(Table.id, String).like(search_like),
                Table.name.like(search_like)
            )
        )

    return query.order_by(Table.sort_order).all()

def get_table_by_name(db: Session, name: str):
    return db.query(Table).filter(Table.name == name).first()

def create_table(db: Session, table: TableCreate):
    existing_table = get_table_by_name(db, table.name)
    if existing_table:
        raise HTTPException(status_code=400, detail="Table already exists")

    sort_order = table.sort_order
    if table.sort_order is None:
        max_sort = db.query(func.max(Table.sort_order)).scalar() or 0
        sort_order = max_sort + 1

    db_table = Table(
        name=table.name,
        capacity=table.capacity,
        note=table.note,
        is_active=table.is_active,
        sort_order=sort_order
    )
    db.add(db_table)
    
    try:
        db.commit()
        db.refresh(db_table)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating table: {str(e)}")

    return db_table
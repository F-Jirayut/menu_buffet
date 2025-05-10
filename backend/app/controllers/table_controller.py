

from app.models import Table
from app.schemas.table import TableCreate, TableUpdate
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status
from sqlalchemy import func, or_, cast, String
from typing import Dict, Optional

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

def get_table_by_id(db: Session, id: int):
    return db.query(Table).filter(Table.id == id).first()

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
        print(str(e))
        raise HTTPException(status_code=500, detail=f"Error creating table: {str(e)}")

    return db_table

def update_table(db: Session, table_id: int, table: TableUpdate) -> Table:
    db_table = db.query(Table).filter(Table.id == table_id).first()
    if not db_table:
        raise HTTPException(status_code=404, detail="Table not found")
    try:
        db_table.name = table.name
        db_table.capacity = table.capacity
        db_table.note = table.note
        db_table.is_active = table.is_active
        db_table.sort_order = table.sort_order
        db.commit()
        db.refresh(db_table)
    except SQLAlchemyError as e:
        db.rollback()
        print(str(e))
        raise HTTPException(status_code=500, detail="Error updating table")
    return db_table

def delete_table(db: Session, table_id: int) -> Dict[str, str]:
    db_table = db.query(Table).filter(Table.id == table_id).first()
    if not db_table:
        raise HTTPException(status_code=404, detail="Table not found")
    try:
        db.delete(db_table)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        print(str(e))
        raise HTTPException(status_code=500, detail="Error deleting table")
    
    return {"message": "Table deleted successfully"}
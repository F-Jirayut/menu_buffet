from typing import List, Optional, Type, Union, Tuple, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import or_, cast, String, desc, asc
from sqlalchemy.ext.declarative import DeclarativeMeta

def get_pagination_items(
    db: Session,
    model: Type[DeclarativeMeta],
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    search_fields: Optional[List[str]] = None,
    order_by: Optional[List[Tuple[str, bool]]] = None,
    options: Optional[List] = None,
    where: Optional[Dict[str, Any]] = None,
) -> List[Union[DeclarativeMeta, dict]]:
    query = db.query(model)

    # Apply eager loading options
    if options:
        for opt in options:
            query = query.options(opt)

    # Apply where conditions
    if where:
        query = query.filter_by(**where)

    # Apply search filter
    if search and search_fields:
        search_conditions = [
            cast(getattr(model, field_name), String).ilike(f"%{search}%")
            for field_name in search_fields
        ]
        query = query.filter(or_(*search_conditions))

    # Apply ordering
    if order_by:
        order_clauses = [
            desc(getattr(model, field)) if is_desc else asc(getattr(model, field))
            for field, is_desc in order_by
        ]
        query = query.order_by(*order_clauses)
    else:
        query = query.order_by(asc(getattr(model, "id")))

    return query.offset(skip).limit(limit).all()

def count_pagination_items(
    db: Session,
    model: Type[DeclarativeMeta],
    search: Optional[str] = None,
    search_fields: Optional[List[str]] = None,
    where: Optional[Dict[str, Any]] = None,  # 👈 เพิ่มตรงนี้
) -> int:
    query = db.query(model)

    if where:
        query = query.filter_by(**where)

    if search and search_fields:
        search_conditions = [
            cast(getattr(model, field_name), String).ilike(f"%{search}%")
            for field_name in search_fields
        ]
        query = query.filter(or_(*search_conditions))

    return query.count()

def parse_order_by_params(order_by: List[str]) -> List[Tuple[str, bool]]:
    parsed: List[Tuple[str, bool]] = []
    for item in order_by:
        parts = item.split(":")
        field = parts[0]
        direction = parts[1].lower() if len(parts) > 1 else "asc"
        is_desc = direction == "desc"
        parsed.append((field, is_desc))
    return parsed

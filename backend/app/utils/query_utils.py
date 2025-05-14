from typing import List, Optional, Type, Union, Tuple
from sqlalchemy.orm import Session, joinedload
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
    options: Optional[List] = None,  # 👈 เพิ่มตรงนี้
) -> List[Union[DeclarativeMeta, dict]]:
    query = db.query(model)

    # Apply eager loading options (เช่น joinedload)
    if options:
        for opt in options:
            query = query.options(opt)

    # Apply search filter
    if search and search_fields:
        search_conditions = []
        for field_name in search_fields:
            field = getattr(model, field_name)
            if str(field.property.columns[0].type) in ["INTEGER", "BIGINT"]:
                field = cast(field, String)
            search_conditions.append(field.ilike(f"%{search}%"))
        query = query.filter(or_(*search_conditions))

    # Apply ordering
    if order_by:
        order_clauses = []
        for field_name, is_desc in order_by:
            order_field = getattr(model, field_name)
            if is_desc:
                order_clauses.append(desc(order_field))
            else:
                order_clauses.append(asc(order_field))
        query = query.order_by(*order_clauses)
    else:
        query = query.order_by(asc(getattr(model, "id")))

    return query.offset(skip).limit(limit).all()

def count_pagination_items(
    db: Session,
    model: Type[DeclarativeMeta],
    search: Optional[str] = None,
    search_fields: Optional[List[str]] = None,
) -> int:
    query = db.query(model)
    if search and search_fields:
        search_conditions = []
        for field_name in search_fields:
            field = getattr(model, field_name)
            if str(field.property.columns[0].type) in ["INTEGER", "BIGINT"]:
                field = cast(field, String)
            search_conditions.append(field.ilike(f"%{search}%"))
        query = query.filter(or_(*search_conditions))
    return query.count()

def parse_order_by_params(order_by: List[str]) -> List[Tuple[str, bool]]:
    """
    แปลง order_by query param เช่น ["name:asc", "created_at:desc"]
    ให้กลายเป็น list ของ tuple (field_name, is_desc)
    """
    parsed: List[Tuple[str, bool]] = []
    for item in order_by:
        parts = item.split(":")
        field = parts[0]
        direction = parts[1].lower() if len(parts) > 1 else "asc"
        is_desc = direction == "desc"
        parsed.append((field, is_desc))
    return parsed

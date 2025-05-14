from app.utils.query_utils import count_pagination_items, get_pagination_items, parse_order_by_params
from sqlalchemy.orm import Session
from typing import List, Optional, Type, Tuple
from sqlalchemy.ext.declarative import DeclarativeMeta

def paginate_controller(
    db: Session,
    model: Type[DeclarativeMeta],
    page: int,
    page_size: int,
    order_by: Optional[List[str]] = None,
    search: Optional[str] = None,
    search_fields: Optional[List[str]] = None,
    options: Optional[list] = None
) -> Tuple[List[DeclarativeMeta], int, int]:
    skip = (page - 1) * page_size
    parsed_order_by = parse_order_by_params(order_by) if order_by else []

    items = get_pagination_items(
        db=db,
        model=model,
        skip=skip,
        limit=page_size,
        search=search,
        search_fields=search_fields or ["id", "name"],
        order_by=parsed_order_by,
        options=options or None,
    )

    total = count_pagination_items(
        db=db,
        model=model,
        search=search,
        search_fields=search_fields or ["id", "name"],
    )

    pages = (total + page_size - 1) // page_size
    return items, total, pages

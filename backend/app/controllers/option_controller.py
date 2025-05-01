from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import MenuCategory, Role, StoreReservationSetting, StoreReservationOverride
from app.schemas.option import OptionResponse
from typing import List, Literal, Optional
from datetime import date

def get_options(type: Literal["categories", "roles"], db: Session) -> List[OptionResponse]:
    if type == "categories":
        model = MenuCategory
    elif type == "roles":
        model = Role
    else:
        raise HTTPException(status_code=400, detail="Invalid type")

    if hasattr(model, "sort_order"):
        items = db.query(model).order_by(model.sort_order, model.id).all()
    else:
        items = db.query(model).order_by(model.id).all()

    return [OptionResponse(id=item.id, name=item.name) for item in items]

def get_store_settings(db: Session):
    settings = db.query(StoreReservationSetting).order_by(StoreReservationSetting.day_of_week).all()
    return settings

def get_store_overrides(db: Session, start_date: Optional[date], end_date: Optional[date]):
    query = db.query(StoreReservationOverride)

    if start_date and end_date:
        query = query.filter(StoreReservationOverride.date.between(start_date, end_date))
    else:
        today = date.today()
        year_start = date(today.year, 1, 1)
        year_end = date(today.year, 12, 31)
        query = query.filter(StoreReservationOverride.date.between(year_start, year_end))

    overrides = query.order_by(StoreReservationOverride.date).all()
    return overrides

from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import MenuCategory, Role
from app.schemas.option import OptionResponse
from typing import List, Literal

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

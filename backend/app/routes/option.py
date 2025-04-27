from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.base_response import BaseResponse
from app.schemas.option import OptionResponse
from app.database import Database
from app.dependencies.auth import get_current_user
from app.controllers import option_controller  # <-- import controller
from typing import List, Literal

db_instance = Database()
get_db = db_instance.get_db
prefix = "/options"

router = APIRouter(
    prefix=prefix,
    tags=["Options"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/", response_model=BaseResponse[List[OptionResponse]])
def get_options(
    type: Literal["categories", "roles"] = Query(..., description="Option type to fetch"),
    db: Session = Depends(get_db),
):
    options = option_controller.get_options(type, db)
    return BaseResponse(
        success=True,
        message="Options fetched successfully",
        data=options
    )

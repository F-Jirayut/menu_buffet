from app.schemas.store_reservation_setting import StoreReservationSettingBase
from app.schemas.store_reservation_override import StoreReservationOverrideBase
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.schemas.base_response import BaseResponse
from app.schemas.option import OptionResponse
from app.database import Database
from app.dependencies.auth import get_current_user
from app.controllers import option_controller  # <-- import controller
from typing import List, Dict, Any, Literal, Optional
from datetime import date

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

@router.get("/store/settings", response_model=BaseResponse[List[StoreReservationSettingBase]])
def get_option_store_settings(db: Session = Depends(get_db)):
    db_store_settings = option_controller.get_store_settings(db)
    # store_settings = [StoreReservationSettingBase.model_validate(setting) for setting in db_store_settings]
    # db_store_overrides = option_controller.get_store_overrides(db)
    # store_overrides = [StoreReservationOverrideBase.model_validate(override) for override in db_store_overrides]

    return BaseResponse(
        success=True,
        message="Store settings fetched successfully",
        data=db_store_settings
    )
    
@router.get("/store/overrides", response_model=BaseResponse[List[StoreReservationOverrideBase]])
def get_option_store_overrides(
    start_date: Optional[date] = Query(None),
    end_date: Optional[date] = Query(None),
    db: Session = Depends(get_db)
):
    db_store_overrides = option_controller.get_store_overrides(db, start_date, end_date)

    return BaseResponse(
        success=True,
        message="Store overrides fetched successfully",
        data=db_store_overrides
    )
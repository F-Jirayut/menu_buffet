from app.controllers import table_controller
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File, Form, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.schemas.table import TableResponse, TableCreate, TableUpdate
from app.schemas.base_response import BaseResponse
from app.database import Database
from app.dependencies.auth import get_current_user
from app.dependencies.user_permission import check_permissions
from typing import List, Optional
import re

db_instance = Database()
get_db = db_instance.get_db
prefix = "/tables"

resource_permissions = {
    "GET": [
        {"pattern": re.compile(f"^{prefix}/$"), "permissions": ["Table.View"]},
        {"pattern": re.compile(f"^{prefix}/[^/]+$"), "permissions": ["Table.View"]},
    ],
    "POST": [
        {"pattern": re.compile(f"^{prefix}/$"), "permissions": ["Table.Create"]}
    ],
    "PUT": [
        {"pattern": re.compile(f"^{prefix}/[^/]+$"), "permissions": ["Table.Update"]}
    ],
    "DELETE": [
        {"pattern": re.compile(f"^{prefix}/[^/]+$"), "permissions": ["Table.Delete"]}
    ]
}

router = APIRouter(
    prefix=prefix,
    tags=["Tables"],
    dependencies=[
        Depends(get_current_user),
        Depends(check_permissions(resource_permissions, get_db))
    ]
)

@router.get("/", response_model=BaseResponse[List[TableResponse]], response_model_exclude_none=True)
def get_tables(db: Session = Depends(get_db), search: Optional[str] = Query(None)):
    
    db_table = table_controller.get_tables(db, search)
    return BaseResponse(
        success=True,
        message="Table fetched successfully",
        data=db_table
    )
    
@router.get("/{table_id}", response_model=BaseResponse[TableResponse], response_model_exclude_none=True)
def table(
    table_id: int,
    db: Session = Depends(get_db)
):
    db_table = table_controller.get_table_by_id(db, id=table_id)
    return BaseResponse(
        success=True,
        message="Table fetched successfully",
        data=db_table
    )
    
@router.post("/", response_model=BaseResponse[TableResponse], response_model_exclude_none=True)
def create_table(table: TableCreate, db: Session = Depends(get_db)):
    db_table = table_controller.create_table(db=db, table=table)
    return BaseResponse(
        success=True,
        message="Table created successfully",
        data=db_table
    )
    
@router.put("/{table_id}", response_model=BaseResponse[TableResponse], response_model_exclude_none=True)
def update_table(table_id: int, table: TableUpdate, db: Session = Depends(get_db)):
    db_table = table_controller.update_table(db=db, table_id=table_id, table=table)
    return BaseResponse(
        success=True,
        message="Table updated successfully",
        data=db_table
    )

@router.delete("/{table_id}", response_model=BaseResponse, response_model_exclude_none=True)
def delete_table(table_id: int, db: Session = Depends(get_db)):
    table_controller.delete_table(db=db, table_id=table_id)
    return BaseResponse(
        success=True,
        message="Table deleted successfully",
        data=None
    )

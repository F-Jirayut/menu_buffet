from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.controllers import role_controller
from app.schemas.role import RoleCreate, Role
from app.database import Database
from app.dependencies.auth import get_current_user
from pydantic import BaseModel

db_instance = Database()
get_db = db_instance.get_db

router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/create", response_model=Role)
def create_role(role: RoleCreate, db: Session = Depends(get_db)):
    return role_controller.create_role(db=db, role=role)

@router.get("/{role_id}", response_model=Role)
def role(role_id: int, db: Session = Depends(get_db)):
    return role_controller.get_role_by_id(db, id=role_id)

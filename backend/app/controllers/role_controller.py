from sqlalchemy.orm import Session
from app.models.role import Role
from app.schemas.role import RoleCreate
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException  # เพิ่มการใช้ HTTPException

def get_role_by_id(db: Session, id: int):
    db_role = db.query(Role).filter(Role.id == id).first()
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

def get_role_by_name(db: Session, name: str):
    return db.query(Role).filter(Role.name == name).first()

def create_role(db: Session, role: RoleCreate):
    existing_role = get_role_by_name(db, role.name)
    if existing_role:
        raise HTTPException(status_code=400, detail="Role name already exists")

    db_role = Role(name=role.name)
    db.add(db_role)
    try:
        db.commit()
        db.refresh(db_role)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating role")
    return db_role

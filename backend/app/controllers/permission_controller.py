from sqlalchemy.orm import Session
from app.models import Permission, RolePermission
from app.schemas.permission import PermissionCreate
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from typing import List, Dict

def get_permission_by_id(db: Session, id: int) -> Permission:
    db_permission = db.query(Permission).order_by(Permission.id).filter(Permission.id == id).first()
    if db_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    return db_permission

def get_permission_by_name(db: Session, name: str) -> Permission:
    return db.query(Permission).order_by(Permission.id).filter(Permission.name == name).first()

def get_permissions(db: Session) -> List[Permission]:
    return db.query(Permission).order_by(Permission.id).all()

def get_grouped_permissions(db_permissions: List[Permission]) -> Dict[str, List[str]]:
    grouped_permissions: Dict[str, List[str]] = {}
    for perm in db_permissions:
        if '.' in perm.name:
            module, action = perm.name.split('.', 1)
            if module not in grouped_permissions:
                grouped_permissions[module] = []
            grouped_permissions[module].append(action)
    return grouped_permissions

def create_permission(db: Session, permission: PermissionCreate) -> Permission:
    existing_permission = get_permission_by_name(db, permission.name)
    if existing_permission:
        raise HTTPException(status_code=400, detail="Permission already exists")

    db_permission = Permission(name=permission.name, description=permission.description)
    db.add(db_permission)
    try:
        db.commit()
        db.refresh(db_permission)
    except SQLAlchemyError as e:
        db.rollback()
        print(str(e))
        raise HTTPException(status_code=500, detail="Error creating permission")
    return db_permission

def update_permission(db: Session, permission_id: int, permission: PermissionCreate) -> Permission:
    db_permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    try:
        db_permission.name = permission.name
        db_permission.description = permission.description
        db.commit()
        db.refresh(db_permission)
    except SQLAlchemyError as e:
        db.rollback()
        print(str(e))
        raise HTTPException(status_code=500, detail="Error updating permission")
    return db_permission

def delete_permission(db: Session, permission_id: int) -> Dict[str, str]:
    db_permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not db_permission:
        raise HTTPException(status_code=404, detail="Permission not found")
    try:
        db.query(RolePermission).filter(RolePermission.permission_id == permission_id).delete()
        db.delete(db_permission)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        print(str(e))
        raise HTTPException(status_code=500, detail="Error deleting permission")
    
    return {"message": "Permission deleted successfully"}

from sqlalchemy.orm import Session, selectinload
from app.models import Role, Permission, RolePermission
from app.schemas.role import RoleCreate
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from typing import Optional, List, Dict, Union

def get_role_by_id(
    db: Session,
    id: int,
    include: Optional[str] = None
) -> Union[Role, Dict]:
    query = db.query(Role).filter(Role.id == id)

    include_items = [item.strip() for item in include.split(',')] if include else []

    if 'permissions' in include_items:
        query = query.options(selectinload(Role.permissions))

    db_role = query.first()

    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")

    if 'permissions_grouped' in include_items:
        return {
            "id": db_role.id,
            "name": db_role.name,
            "permissions_by_module": get_grouped_permissions(db_role.permissions)
        }

    return db_role

def get_grouped_permissions(db_permissions: List[Permission]) -> Dict[str, List[str]]:
    grouped_permissions: Dict[str, List[str]] = {}
    for perm in db_permissions:
        if '.' in perm.name:
            module, action = perm.name.split('.', 1)
            if module not in grouped_permissions:
                grouped_permissions[module] = []
            grouped_permissions[module].append(action)
    return grouped_permissions


def get_role_by_name(db: Session, name: str):
    return db.query(Role).filter(Role.name == name).first()

def get_roles(db: Session):
    return db.query(Role).all()

def create_role(db: Session, role: RoleCreate):
    existing_role = get_role_by_name(db, role.name)
    if existing_role:
        raise HTTPException(status_code=400, detail="Role already exists")

    permission_names = role.permission_names or []

    permissions = db.query(Permission).filter(Permission.name.in_(permission_names)).all() if permission_names else []

    db_role = Role(name=role.name, permissions=permissions)
    db.add(db_role)

    try:
        db.commit()
        db.refresh(db_role)
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating role: {str(e)}")

    return db_role

def update_role(db: Session, role_id: int, role: RoleCreate):
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")

    db_role.name = role.name

    permission_names = role.permission_names or []
    if permission_names:
        permissions = db.query(Permission).filter(Permission.name.in_(permission_names)).all()
        db_role.permissions = permissions
    else:
        db_role.permissions = []
    try:
        db.commit()
        db.refresh(db_role)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error updating role")

    return db_role

def delete_role(db: Session, role_id: int):
    db_role = db.query(Role).filter(Role.id == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    try:
        db.query(RolePermission).filter(RolePermission.role_id == role_id).delete()
        db.delete(db_role)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Error deleting role")
    
    return {"message": "Role deleted successfully"}

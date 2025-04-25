import re
from fastapi import Request, Depends
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_403_FORBIDDEN
from sqlalchemy.orm import Session, joinedload
from app.models import User, Role
from app.dependencies.auth import get_current_user

def check_permissions(resource_permissions: dict, get_db):
    def dependency(
        request: Request,
        payload=Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        user = (
            db.query(User)
            .filter(User.id == payload.get("id"))
            .options(joinedload(User.role).joinedload(Role.permissions))  # eager load
            .first()
        )

        if not user or not user.role:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid user or role.")

        method = request.method
        path = request.url.path

        permissions_required = []
        if method in resource_permissions:
            for rule in resource_permissions[method]:
                if rule["pattern"].match(path):
                    permissions_required = rule["permissions"]
                    break

        if not permissions_required:
            return  # ไม่มี permission ที่ต้องเช็ค

        user_permissions = {perm.name for perm in user.role.permissions}

        if not any(p in user_permissions for p in permissions_required):
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action."
            )

    return dependency

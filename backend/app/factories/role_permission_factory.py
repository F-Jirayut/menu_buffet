
from app.database import SessionLocal
from app.models.role import Role
from app.models.permission import Permission

class RolePermissionFactory:
    @staticmethod
    def assign(role: Role, permission: Permission):
        session = SessionLocal()
        role.permissions.append(permission)
        session.add(role)
        session.commit()
        session.refresh(role)
        return role

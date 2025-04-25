
from app.models.permission import Permission
from app.database import SessionLocal
import random

class PermissionFactory:
    @staticmethod
    def create(name=None, description=None):
        session = SessionLocal()
        permission = Permission(
            name=name or f"perm_{random.randint(1, 1000)}",
            description=description or "Test permission"
        )
        session.add(permission)
        session.commit()
        session.refresh(permission)
        return permission

    @staticmethod
    def build(name=None, description=None):
        return Permission(
            name=name or f"perm_{random.randint(1, 1000)}",
            description=description or "Test permission"
        )

from app.models.role import Role
from app.database import SessionLocal
import random

class RoleFactory:
    @staticmethod
    def create(name=None):
        # สร้างข้อมูล role ใหม่
        session = SessionLocal()
        role = Role(name=name or f"Role_{random.randint(1, 1000)}")
        session.add(role)
        session.commit()
        session.refresh(role)
        return role

    @staticmethod
    def build(name=None):
        # สร้างข้อมูล role ใน memory
        return Role(name=name or f"Role_{random.randint(1, 1000)}")

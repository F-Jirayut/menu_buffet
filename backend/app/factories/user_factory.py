from app.models.user import User
from app.database import SessionLocal
from app.models.role import Role
from app.factories.role_factory import RoleFactory
import random

class UserFactory:
    @staticmethod
    def create(name=None, username=None, password=None, role=None):
        # สร้างข้อมูล user ใหม่
        session = SessionLocal()

        # หากไม่ระบุ role จะสร้าง role ใหม่จาก RoleFactory
        role = role or RoleFactory.create()

        user = User(
            name=name or f"User_{random.randint(1, 1000)}",
            username=username or f"username_{random.randint(1, 1000)}",
            password=password or f"password_{random.randint(1, 1000)}",
            role_id=role.id
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def build(name=None, username=None, password=None, role=None):
        # สร้างข้อมูล user ใน memory
        role = role or RoleFactory.build()

        return User(
            name=name or f"User_{random.randint(1, 1000)}",
            username=username or f"username_{random.randint(1, 1000)}",
            password=password or f"password_{random.randint(1, 1000)}",
            role_id=role.id
        )

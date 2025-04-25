from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base
from sqlalchemy.orm import relationship

class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), server_default=func.now())

    roles = relationship("Role", secondary="role_permissions",back_populates="permissions")
    
    # roles = relationship("Role", secondary="role_permissions",back_populates="permissions", overlaps="role_permissions")
    # role_permissions = relationship("RolePermission", back_populates="permission", cascade="all, delete", overlaps="permissions,roles")


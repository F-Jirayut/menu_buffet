from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base
from sqlalchemy.orm import relationship

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), server_default=func.now())
    
    users = relationship("User", back_populates="role")
    permissions = relationship('Permission', secondary='role_permissions', back_populates='roles', order_by='Permission.id')
    
    # role_permissions = relationship("RolePermission", back_populates="role", cascade="all, delete", overlaps="permissions,roles")
    # permissions = relationship("Permission", secondary="role_permissions",backref="roles")

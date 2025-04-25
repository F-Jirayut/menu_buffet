from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from app.database import Base
from sqlalchemy.orm import relationship

class RolePermission(Base):
    __tablename__ = 'role_permissions'

    role_id = Column(Integer, ForeignKey('roles.id', ondelete='CASCADE'), primary_key=True)
    permission_id = Column(Integer, ForeignKey('permissions.id', ondelete='CASCADE'), primary_key=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), server_default=func.now())

    # role_privot = relationship("Role", back_populates="role_permission_pivot")
    # permission_pivot = relationship("Permission", back_populates="role_permission_pivot")
    # role_privot = relationship("Role", back_populates="permissions")
    # permission = relationship("Permission", back_populates="roles")
    # role = relationship("Role", backref="role_permissions")
    # permission = relationship("Permission", backref="role_permissions")
    # role = relationship("Role", back_populates="role_permissions", overlaps="permissions,roles")
    # permission = relationship("Permission", back_populates="role_permissions", overlaps="permissions,roles")
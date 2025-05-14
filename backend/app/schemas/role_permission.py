from pydantic import BaseModel, ConfigDict
from typing import Optional

class RolePermissionBase(BaseModel):
    role_id: int
    permission_id: int
    
    model_config = ConfigDict(
        extra='ignore',
        populate_by_name=True,
        str_strip_whitespace=True,
        from_attributes=True,
        exclude_none=True
    )

class RolePermissionCreate(RolePermissionBase):
    pass

class RolePermission(RolePermissionBase):
    id: int
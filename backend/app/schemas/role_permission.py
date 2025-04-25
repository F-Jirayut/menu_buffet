from pydantic import BaseModel
from typing import Optional

class RolePermissionBase(BaseModel):
    role_id: int
    permission_id: int

class RolePermissionCreate(RolePermissionBase):
    pass

class RolePermission(RolePermissionBase):
    id: int

    model_config = {
        "from_attributes": True
    }
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from app.schemas.permission import Permission

class RoleBase(BaseModel):
    name: str
    
    model_config = ConfigDict(
        extra='ignore',
        populate_by_name=True,
        str_strip_whitespace=True,
        from_attributes=True,
        exclude_none=True
    )

class RoleCreate(RoleBase):
    name: str
    permission_names: Optional[List[str]] = None

class RoleCreateWithPermissions(RoleBase):
    permission_ids: List[int]


class Role(RoleBase):
    id: int
    permissions: Optional[List[Permission]] = None
    permissions_by_module: Optional[dict] = None

class RoleDeleteResponse(BaseModel):
    message: str
    role_id: int

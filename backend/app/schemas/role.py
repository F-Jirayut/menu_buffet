from pydantic import BaseModel
from typing import List, Optional
from app.schemas.permission import Permission

class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    name: str
    permission_names: Optional[List[str]] = None

class RoleCreateWithPermissions(RoleBase):
    permission_ids: List[int]


class Role(RoleBase):
    id: int
    permissions: Optional[List[Permission]] = None
    permissions_by_module: Optional[dict] = None

    model_config = {
        "from_attributes": True
    }

class RoleDeleteResponse(BaseModel):
    message: str
    role_id: int

    model_config = {
        "from_attributes": True
    }

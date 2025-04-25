from pydantic import BaseModel, RootModel, validator
from typing import List, Optional, Dict
import re

class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None


class PermissionCreate(PermissionBase):
    @validator('name')
    def validate_name_suffix(cls, v):
        if not re.search(r'\.(View|Create|Update|Delete)$', v):
            raise ValueError("name must end with .View, .Create, .Update, or .Delete")
        return v


class Permission(PermissionBase):
    id: int

    model_config = {
        "from_attributes": True
    }

class GroupedPermissions(RootModel[Dict[str, List[str]]]):
    pass

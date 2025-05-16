from pydantic import BaseModel, RootModel, validator, ConfigDict
from typing import List, Optional, Dict
import re

class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None
    
    model_config = ConfigDict(
        extra='ignore',
        populate_by_name=True,
        str_strip_whitespace=True,
        from_attributes=True,
        exclude_none=True
    )


class PermissionCreate(PermissionBase):
    @validator('name')
    def validate_name_suffix(cls, v):
        if not re.search(r'\.(View|Create|Update|Delete)$', v):
            raise ValueError("name must end with .View, .Create, .Update, or .Delete")
        return v


class Permission(PermissionBase):
    id: int

class GroupedPermissions(RootModel[Dict[str, List[str]]]):
    pass

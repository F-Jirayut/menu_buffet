from pydantic import BaseModel, EmailStr, constr, validator, ConfigDict
from typing import Optional
from datetime import datetime


class CustomerBase(BaseModel):
    name: str
    phone: constr(min_length=10, max_length=10)
    email: Optional[EmailStr] = None
    
    model_config = ConfigDict(
        extra='ignore',
        populate_by_name=True,
        str_strip_whitespace=True,
        from_attributes=True,
        exclude_none=True
    )
    
    @validator('phone')
    def validate_phone(cls, v):
        if not v.isdigit():
            raise ValueError('Phone must be numeric.')
        if len(v) < 10:
            raise ValueError('Phone must be at least 10 digits.')
        return v


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(CustomerBase):
    pass
    
class CustomerResponse(CustomerBase):
    id: int
    pass


class CustomerInDB(CustomerBase):
    id: int
    email_sent: bool
    created_at: datetime
    updated_at: datetime

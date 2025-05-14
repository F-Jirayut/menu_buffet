from pydantic import BaseModel, ConfigDict

class OptionResponse(BaseModel):
    id: int
    name: str
    
    model_config = ConfigDict(
        extra='ignore',
        populate_by_name=True,
        str_strip_whitespace=True,
        from_attributes=True,
        exclude_none=True
    )

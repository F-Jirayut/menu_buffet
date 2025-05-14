from pydantic import BaseModel, ConfigDict

class Pagination(BaseModel):
    page: int
    page_size: int
    total: int
    pages: int
    
    model_config = ConfigDict(
        extra='ignore',
        populate_by_name=True,
        str_strip_whitespace=True,
        from_attributes=True,
        exclude_none=True
    )

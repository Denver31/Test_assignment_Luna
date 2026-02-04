from typing import Optional

from pydantic import BaseModel, Field


class BaseActivitySchema(BaseModel):
    name: str = Field(..., description="Название деятельности")
    parent_id: Optional[int] = None


class AddActivitySchema(BaseActivitySchema):
    pass


class ReadActivitySchema(BaseActivitySchema):
    id: int

    class Config:
        from_attributes = True

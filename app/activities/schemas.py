from typing import Optional

from pydantic import BaseModel


class BaseActivitySchema(BaseModel):
    name: str
    parent_id: Optional[int] = None


class AddActivitySchema(BaseActivitySchema):
    pass


class ReadActivitySchema(BaseActivitySchema):
    id: int

    class Config:
        from_attributes = True

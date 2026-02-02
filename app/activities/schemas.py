from typing import Optional

from pydantic import BaseModel


class AddActivitySchema(BaseModel):
    name: str
    parent_id: Optional[int] = None

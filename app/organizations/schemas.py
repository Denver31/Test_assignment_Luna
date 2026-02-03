from pydantic import BaseModel, Field

from app.activities.schemas import ReadActivitySchema
from app.buildings.schemas import ReadBuildingSchema
from app.organizations.phones.schemas import ReadPhoneSchema


class BaseOrganizationSchema(BaseModel):
    name: str = Field(..., max_length=16, description="Имя организации")
    building_id: int = Field(..., description="id здания")


class AddOrganizationSchema(BaseOrganizationSchema):
    pass


class ReadOrganizationSchema(BaseOrganizationSchema):
    id: int

    class Config:
        from_attributes = True


class ReadFullOrganizationSchema(ReadOrganizationSchema):
    phones: list[ReadPhoneSchema]
    building: ReadBuildingSchema
    activities: list[ReadActivitySchema]

    class Config:
        from_attributes = True

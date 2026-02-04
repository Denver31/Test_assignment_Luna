from pydantic import BaseModel, Field, model_validator

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


class RadiusQuery(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    radius: float = Field(..., gt=0)


class BoxQuery(BaseModel):
    min_lat: float = Field(..., ge=-90, le=90)
    max_lat: float = Field(..., ge=-90, le=90)
    min_lon: float = Field(..., ge=-180, le=180)
    max_lon: float = Field(..., ge=-180, le=180)

    @model_validator(mode="after")
    def check_bounds(self):
        if self.min_lat > self.max_lat:
            raise ValueError("min_lat must be <= max_lat")
        if self.min_lon > self.max_lon:
            raise ValueError("min_lon must be <= max_lon")
        return self

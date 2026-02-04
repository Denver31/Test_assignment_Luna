from pydantic import BaseModel, Field


class BaseBuildingSchema(BaseModel):
    address: str = Field(..., description="Адрес здания")

    latitude: float = Field(..., ge=-90, le=90, description="Широта в градусах от -90 до 90")
    longitude: float = Field(..., ge=-180, le=180, description="Долгота в градусах от -180 до 180")


class AddBuildingSchema(BaseBuildingSchema):
    pass


class ReadBuildingSchema(BaseBuildingSchema):
    id: int

    class Config:
        from_attributes = True

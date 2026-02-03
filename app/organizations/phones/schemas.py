from pydantic import BaseModel, Field


class BasePhoneSchema(BaseModel):
    phone: str = Field(..., max_length=16, description="Номер телефона")
    organization_id: int = Field(..., description="id организации")


class AddPhoneSchema(BasePhoneSchema):
    pass


class ReadPhoneSchema(BasePhoneSchema):
    id: int

    class Config:
        from_attributes = True

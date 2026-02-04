from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.organizations.phones.dao import PhoneDAO
from app.organizations.phones.schemas import AddPhoneSchema, ReadPhoneSchema

router = APIRouter(
    prefix="/organizations/phones",
    tags=["Organization's phones"]
)


@router.post("", response_model=ReadPhoneSchema)
async def add_phone(data: AddPhoneSchema, session: AsyncSession = Depends(get_session)) -> ReadPhoneSchema:
    """Добавить номер телефона"""
    dao = PhoneDAO(session)
    try:
        phone = await dao.add(phone=data.phone, organization_id=data.organization_id)
        return phone
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
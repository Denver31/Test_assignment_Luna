from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.organizations.model import Organization
from app.organizations.phones.model import Phone


class PhoneDAO(BaseDAO):
    model = Phone

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def add(self, phone: str, organization_id: int):
        org = await self.session.get(Organization, organization_id)
        if org is None:
            raise ValueError(f"Organization with id {organization_id} not found")

        phone = Phone(phone=phone, organization_id=organization_id)

        self.session.add(phone)
        await self.session.flush()

        return phone

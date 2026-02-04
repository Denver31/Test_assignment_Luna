from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.activities.model import Activity
from app.buildings.model import Building
from app.dao.base import BaseDAO
from app.organizations.model import Organization


class OrganizationDAO(BaseDAO):
    model = Organization

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def add(self, name: str, building_id: int) -> Organization:
        building = await self.session.get(Building, building_id)
        if building is None:
            raise ValueError(f"Building with id {building_id} not found")

        organization = Organization(name=name, building_id=building_id)

        self.session.add(organization)
        await self.session.flush()

        return organization

    async def get_all(self) -> list[Organization]:
        result = await self.session.execute(
            select(self.model).options(
                selectinload(self.model.activities),
                selectinload(self.model.building),
                selectinload(self.model.phones)
            ))
        return result.scalars().all()

    async def get_by_activity(self, activity_id) -> list[Organization]:
        stmt = (
            select(Organization)
            .where(
                Organization.activities.any(Activity.id == activity_id)
            )
            .options(
                selectinload(Organization.building),
                selectinload(Organization.phones),
                selectinload(Organization.activities),
            )
        )

        res = await self.session.execute(stmt)
        return res.scalars().all()

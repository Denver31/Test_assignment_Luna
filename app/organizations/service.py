from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.activities.model import Activity
from app.organizations.dao import OrganizationDAO
from app.organizations.model import Organization


class OrganizationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_organisation(self, name: str, building_id: int):
        dao = OrganizationDAO(self.session)
        return await dao.add(name, building_id)

    async def add_activity_to_organization(self, organization_id: int, activity_id: int) -> Organization:
        organization = await self.session.get(Organization, organization_id)
        if organization is None:
            raise ValueError(f"Organization with id {organization_id} not found")

        activity = await self.session.get(Activity, activity_id)
        if activity is None:
            raise ValueError(f"Activity with id {activity_id} not found")

        if activity in organization.activities:
            return organization

        organization.activities.append(activity)
        await self.session.flush()
        return organization

    async def get_all_organizations(self):
        dao = OrganizationDAO(self.session)
        return await dao.get_all()

    async def get_organizations_by_building(self, building_id: int) -> List[Organization]:
        dao = OrganizationDAO(self.session)
        organizations = dao.find_all(building_id=building_id)
        return organizations

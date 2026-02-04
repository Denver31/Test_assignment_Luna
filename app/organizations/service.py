from sqlalchemy.ext.asyncio import AsyncSession

from app.activities.dao import ActivityDAO
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

    async def get_organizations_by_building(self, building_id: int) -> list[Organization]:
        dao = OrganizationDAO(self.session)
        organizations = await dao.find_all(building_id=building_id)
        return organizations

    async def get_organization_by_activity(self, activity_id: int) -> list[Organization]:
        dao = OrganizationDAO(self.session)
        organizations = await dao.get_by_activity(activity_id=activity_id)
        return organizations

    async def get_organizations_in_radius(self, lat: float, lon, radius: float) -> list[Organization]:
        dao = OrganizationDAO(self.session)
        if lat < -90 or lat > 90:
            raise ValueError("Invalid latitude")
        if lon < -180 or lon > 180:
            raise ValueError("Invalid longitude")
        return await dao.get_organizations_in_radius(lat, lon, radius)

    async def get_organizations_in_box(self, min_lat: float, max_lat: float,
                                       min_lon: float, max_lon: float) -> list[Organization]:
        if min_lat > max_lat or min_lon > max_lon:
            raise ValueError("Invalid bounding box")
        dao = OrganizationDAO(self.session)
        return await dao.get_organizations_in_box(min_lat, max_lat, min_lon, max_lon)

    async def get_organization_by_id(self, organization_id: int) -> Organization:
        organization = await self.session.get(Organization, organization_id)
        if organization is None:
            raise ValueError(f"Organization with id {organization_id} not found")
        return organization

    async def find_organizations_by_activity(self, activity_id: int) -> list[Organization]:
        activity_dao = ActivityDAO(self.session)
        organization_dao = OrganizationDAO(self.session)

        activities = await activity_dao.get_activity_tree(activity_id)
        organizations = await organization_dao.get_by_activities([act.id for act in activities])
        return organizations

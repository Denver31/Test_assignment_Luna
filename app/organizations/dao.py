import math

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

    async def get_organizations_in_box(
            self,
            min_lat: float,
            max_lat: float,
            min_lon: float,
            max_lon: float,
    ) -> list[Organization]:
        stmt = (
            select(Organization)
            .join(Organization.building)
            .where(
                Building.latitude.between(min_lat, max_lat),
                Building.longitude.between(min_lon, max_lon),
            )
        )

        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_organizations_in_radius(
            self,
            lat: float,
            lon: float,
            radius: float,
    ) -> list[Organization]:
        """
        :param lon: долгота в градусах
        :param lat: широта в градусах
        :param radius: радиус в км
        """

        lat_delta = radius / 111
        lon_delta = radius / (111 * math.cos(math.radians(lat)))

        stmt = (
            select(Organization)
            .join(Organization.building)
            .where(
                Building.latitude.between(lat - lat_delta, lat + lat_delta),
                Building.longitude.between(lon - lon_delta, lon + lon_delta),
                self.haversine_distance_expr(
                    lat,
                    lon,
                    Building.latitude,
                    Building.longitude,
                ) <= radius,
            )
        )

        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_by_activities(self, activity_ids: list[int]) -> list[Organization]:
        if not activity_ids:
            return []

        stmt = (
            select(Organization)
            .where(
                Organization.activities.any(Activity.id.in_(activity_ids))
            )
            .options(
                selectinload(Organization.building),
                selectinload(Organization.phones),
                selectinload(Organization.activities),
            )
        )

        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_by_name(self, name: str) -> list[Organization]:

        if len(name) < 3:
            raise ValueError("Name should be at least 3 characters long")

        res = await self.session.execute((
            select(Organization)
            .where(Organization.name.ilike(f"%{name}%"))
        ))

        return res.scalars().all()

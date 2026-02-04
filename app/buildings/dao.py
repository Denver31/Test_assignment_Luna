import math

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.buildings.model import Building
from app.dao.base import BaseDAO


class BuildingDAO(BaseDAO):
    model = Building

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def add(self, address: str, latitude: float, longitude: float) -> Building:
        building = Building(address=address, latitude=latitude, longitude=longitude)

        self.session.add(building)
        await self.session.flush()

        return building

    async def get_buildings_in_box(self, min_lat: float, max_lat: float,
                                   min_lon: float, max_lon: float) -> list[Building]:
        stmt = (
            select(Building)
            .where(
                Building.latitude.between(min_lat, max_lat),
                Building.longitude.between(min_lon, max_lon),
            )
        )
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def get_buildings_in_radius(self, lat: float, lon, radius: float) -> list[Building]:
        """
        :param lon: долгота в градусах
        :param lat: широта в градусах
        :param radius: Радиус в км
        """
        lat_delta = radius / 111
        lon_delta = radius / (111 * math.cos(math.radians(lat)))

        stmt = (
            select(Building)
            .where(
                Building.latitude.between(lat - lat_delta, lat + lat_delta),
                Building.longitude.between(lon - lon_delta, lon + lon_delta),
                self.haversine_distance_expr(lat, lon, Building.latitude, Building.longitude) <= radius
            )
        )
        res = await self.session.execute(stmt)
        return res.scalars().all()

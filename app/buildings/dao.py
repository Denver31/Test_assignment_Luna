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


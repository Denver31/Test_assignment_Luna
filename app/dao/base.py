from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def find_all(self, **filters):
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)
        return result.scalars().all()

    @staticmethod
    def haversine_distance_expr(lat, lon, lat_col, lon_col):
        return (
                6371 * func.acos(
            func.cos(func.radians(lat)) *
            func.cos(func.radians(lat_col)) *
            func.cos(func.radians(lon_col) - func.radians(lon)) +
            func.sin(func.radians(lat)) *
            func.sin(func.radians(lat_col))
        )
        )

from sqlalchemy import select
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

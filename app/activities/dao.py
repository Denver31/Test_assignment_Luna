from sqlalchemy.ext.asyncio import AsyncSession

from app.activities.model import Activity
from app.dao.base import BaseDAO


class ActivityDao(BaseDAO):
    model = Activity

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def add(self, name, parent_id: int | None = None) -> Activity:
        level = 1

        if parent_id:
            parent: Activity | None = await self.session.get(Activity, parent_id)
            if not parent:
                raise ValueError(f"Parent activity with id {parent_id} not found")
            if parent.level >= 3:
                raise ValueError("Cannot assign this activity to the specified parent: the maximum nesting level is 3")

            level = parent.level + 1

        activity = Activity(name=name, parent_id=parent_id, level=level)

        self.session.add(activity)
        await self.session.flush()

        return activity

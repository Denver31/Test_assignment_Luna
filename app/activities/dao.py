from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.activities.model import Activity
from app.dao.base import BaseDAO


class ActivityDAO(BaseDAO):
    model = Activity

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def add(self, name: str, parent_id: int | None = None) -> Activity:
        level = 1
        if parent_id is not None:
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

    async def get_activities_by_parents(self, parent_ids: list[int]) -> list[Activity]:
        res = await self.session.execute(
            select(self.model)
            .where(self.model.parent_id.in_(parent_ids))
        )
        return res.scalars().all()

    async def get_activity_tree(self, parent_id: int) -> list[Activity]:
        """Получает дерево активностей начиная с родителя"""
        parent = await self.session.get(Activity, parent_id)
        if parent is None:
            raise ValueError(f"Activity with id {parent_id} not found")

        result: list[Activity] = [parent]
        current_level_ids: list[int] = [parent_id]

        while current_level_ids:
            children = await self.get_activities_by_parents(current_level_ids)
            if not children:
                break
            result.extend(children)
            current_level_ids = [child.id for child in children]

        return result

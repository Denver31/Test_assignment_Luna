from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.activities.dao import ActivityDao
from app.activities.schemas import AddActivitySchema
from app.database import get_session

router = APIRouter(
    prefix="/activities",
    tags=["activities"]
)


@router.post("/add")
async def add_activity(data: AddActivitySchema, session: AsyncSession = Depends(get_session)):
    dao = ActivityDao(session)
    try:
        activity = await dao.add(data.name, data.parent_id)
        await session.commit()
        return activity
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/all")
async def get_all_activities(session: AsyncSession = Depends(get_session)):
    dao = ActivityDao(session)
    return await dao.get_all()

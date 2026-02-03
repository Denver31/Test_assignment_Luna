from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.activities.dao import ActivityDAO
from app.activities.schemas import AddActivitySchema, ReadActivitySchema
from app.database import get_session

router = APIRouter(
    prefix="/activities",
    tags=["Activities"]
)


@router.post("/add", response_model=ReadActivitySchema)
async def add_activity(data: AddActivitySchema, session: AsyncSession = Depends(get_session)) -> ReadActivitySchema:
    dao = ActivityDAO(session)
    try:
        activity = await dao.add(data.name, data.parent_id)
        return activity
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/all", response_model=list[ReadActivitySchema])
async def get_all_activities(session: AsyncSession = Depends(get_session)) -> list[ReadActivitySchema]:
    dao = ActivityDAO(session)
    return await dao.get_all()

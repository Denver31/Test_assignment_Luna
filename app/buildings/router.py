from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.buildings.dao import BuildingDAO
from app.buildings.schemas import ReadBuildingSchema, AddBuildingSchema
from app.database import get_session

router = APIRouter(
    prefix="/buildings",
    tags=["Buildings"]
)


@router.post("", response_model=ReadBuildingSchema)
async def add_building(data: AddBuildingSchema, session: AsyncSession = Depends(get_session)) -> ReadBuildingSchema:
    dao = BuildingDAO(session)
    building = await dao.add(address=data.address, latitude=data.latitude, longitude=data.longitude)
    return building


@router.get("", response_model=list[ReadBuildingSchema])
async def get_all_buildings(session: AsyncSession = Depends(get_session)) -> list[ReadBuildingSchema]:
    dao = BuildingDAO(session)
    return await dao.get_all()

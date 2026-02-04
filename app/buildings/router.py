from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.buildings.dao import BuildingDAO
from app.buildings.schemas import ReadBuildingSchema, AddBuildingSchema
from app.database import get_session
from app.organizations.schemas import ReadFullOrganizationSchema, RadiusQuery, BoxQuery
from app.organizations.service import OrganizationService

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


@router.get("/{building_id}/organizations", response_model=list[ReadFullOrganizationSchema])
async def get_organizations_by_building(building_id: int, session: AsyncSession = Depends(get_session)):
    service = OrganizationService(session)
    return await service.get_organizations_by_building(building_id)


@router.get("/geo/radius", response_model=list[ReadBuildingSchema])
async def get_buildings_in_radius(query: RadiusQuery = Depends(), session: AsyncSession = Depends(get_session)):
    dao = BuildingDAO(session)
    return await dao.get_buildings_in_radius(**query.model_dump())


@router.get("/geo/box", response_model=list[ReadBuildingSchema])
async def get_buildings_in_box(query: BoxQuery = Depends(), session: AsyncSession = Depends(get_session)):
    dao = BuildingDAO(session)
    return await dao.get_buildings_in_box(**query.model_dump())

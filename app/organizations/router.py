from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.organizations.schemas import AddOrganizationSchema, ReadOrganizationSchema, ReadFullOrganizationSchema, \
    RadiusQuery, BoxQuery
from app.organizations.service import OrganizationService

router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"]
)


@router.post("", response_model=ReadOrganizationSchema)
async def add_organization(data: AddOrganizationSchema,
                           session: AsyncSession = Depends(get_session)) -> ReadOrganizationSchema:
    service = OrganizationService(session)
    try:
        organization = await service.add_organisation(name=data.name, building_id=data.building_id)
        return organization
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{organization_id}/activities/{activity_id}", response_model=ReadFullOrganizationSchema)
async def add_activity_to_organization(organization_id: int, activity_id: int,
                                       session: AsyncSession = Depends(get_session)):
    try:
        service = OrganizationService(session)
        organization = await service.add_activity_to_organization(organization_id, activity_id)
        return organization
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[ReadFullOrganizationSchema])
async def get_all_organizations(session: AsyncSession = Depends(get_session)):
    service = OrganizationService(session)
    return await service.get_all_organizations()


@router.get("/geo/radius", response_model=list[ReadFullOrganizationSchema])
async def get_organizations_in_radius(query: RadiusQuery = Depends(), session: AsyncSession = Depends(get_session)):
    service = OrganizationService(session)
    return await service.get_organizations_in_radius(**query.model_dump())


@router.get("/geo/box", response_model=list[ReadFullOrganizationSchema])
async def get_organizations_in_radius(query: BoxQuery = Depends(), session: AsyncSession = Depends(get_session)):
    service = OrganizationService(session)
    return await service.get_organizations_in_box(**query.model_dump())

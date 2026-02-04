from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.activities.dao import ActivityDAO
from app.activities.schemas import AddActivitySchema, ReadActivitySchema
from app.database import get_session
from app.organizations.schemas import ReadFullOrganizationSchema
from app.organizations.service import OrganizationService

router = APIRouter(
    prefix="/activities",
    tags=["Activities"]
)


@router.post("", response_model=ReadActivitySchema)
async def add_activity(data: AddActivitySchema, session: AsyncSession = Depends(get_session)) -> ReadActivitySchema:
    """Создать новую активность"""
    dao = ActivityDAO(session)
    try:
        activity = await dao.add(data.name, data.parent_id)
        return activity
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[ReadActivitySchema])
async def get_all_activities(session: AsyncSession = Depends(get_session)) -> list[ReadActivitySchema]:
    """Получить все активности"""
    dao = ActivityDAO(session)
    return await dao.get_all()


@router.get("/{activity_id}/organizations", response_model=list[ReadFullOrganizationSchema])
async def get_organizations_by_activity(activity_id: int,
                                        session: AsyncSession = Depends(get_session)) -> ReadActivitySchema:
    """Получить все организации по конкретной активности"""
    service = OrganizationService(session)
    return await service.get_organization_by_activity(activity_id=activity_id)


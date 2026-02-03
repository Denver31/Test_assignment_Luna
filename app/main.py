from fastapi import FastAPI

from app.activities.router import router as activities_router
from app.buildings.router import router as buildings_router
from app.organizations.router import router as organizations_router
from app.organizations.phones.router import router as phones_router

app = FastAPI()

app.include_router(activities_router)
app.include_router(buildings_router)
app.include_router(phones_router)
app.include_router(organizations_router)
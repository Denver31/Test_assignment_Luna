from fastapi import FastAPI

from app.activities.router import router as activities_router
from app.buildings.router import router as buildings_router

app = FastAPI()

app.include_router(activities_router)
app.include_router(buildings_router)

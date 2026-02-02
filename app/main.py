from fastapi import FastAPI

from app.activities.router import router as activities_router

app = FastAPI()

app.include_router(activities_router)

import asyncio
import json
from pathlib import Path

from sqlalchemy import text

from app.activities.model import Activity
from app.buildings.model import Building
from app.database import async_session_maker
from app.organizations.m2m import organization_activity
from app.organizations.model import Organization
from app.organizations.phones.model import Phone

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"


def load_json(filename: str) -> list[dict]:
    with open(DATA_DIR / filename, encoding="utf-8") as f:
        return json.load(f)


def without_id(data: dict) -> dict:
    return {k: v for k, v in data.items() if k != "id"}


async def clear_db(session):
    await session.execute(text("""
                               TRUNCATE TABLE
                                   organization_activity,
            phones,
            organizations,
            activities,
            buildings
        RESTART IDENTITY CASCADE
                               """))


async def seed():
    async with async_session_maker() as session:
        await clear_db(session)

        buildings = [
            Building(**without_id(data))
            for data in load_json("buildings.json")
        ]
        session.add_all(buildings)

        activities = [
            Activity(**without_id(data))
            for data in load_json("activities.json")
        ]
        session.add_all(activities)

        organizations = [
            Organization(**without_id(data))
            for data in load_json("organizations.json")
        ]
        session.add_all(organizations)

        await session.flush()

        await session.execute(
            organization_activity.insert(),
            load_json("organization_activities.json")
        )

        phones = [
            Phone(**without_id(data))
            for data in load_json("phones.json")
        ]
        session.add_all(phones)

        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())

import asyncio
import json
from pathlib import Path

from sqlalchemy import text

from app.database import async_session_maker
from app.buildings.model import Building
from app.activities.model import Activity
from app.organizations.model import Organization
from app.organizations.phones.model import Phone
from app.organizations.m2m import organization_activity

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"


def load_json(filename: str) -> list[dict]:
    with open(DATA_DIR / filename, encoding="utf-8") as f:
        return json.load(f)


async def clear_db(session):
    await session.execute(text("TRUNCATE TABLE organization_activity CASCADE"))
    await session.execute(text("TRUNCATE TABLE phones CASCADE"))
    await session.execute(text("TRUNCATE TABLE organizations CASCADE"))
    await session.execute(text("TRUNCATE TABLE activities CASCADE"))
    await session.execute(text("TRUNCATE TABLE buildings CASCADE"))


async def seed():
    async with async_session_maker() as session:
        await clear_db(session)

        buildings = [
            Building(**data)
            for data in load_json("buildings.json")
        ]
        session.add_all(buildings)

        activities = [
            Activity(**data)
            for data in load_json("activities.json")
        ]
        session.add_all(activities)

        organizations = [
            Organization(**data)
            for data in load_json("organizations.json")
        ]
        session.add_all(organizations)

        await session.flush()

        m2m_data = load_json("organization_activities.json")
        await session.execute(
            organization_activity.insert(),
            m2m_data
        )
        phones = [
            Phone(**data)
            for data in load_json("phones.json")
        ]
        session.add_all(phones)

        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())

import pytest
import pytest_asyncio
from httpx import AsyncClient
from tortoise import Tortoise

from app.main import app


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():
    await Tortoise.init(
        db_url="sqlite://db.sqlite3", modules={"models": ["app.models"]}
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise.close_connections()


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client

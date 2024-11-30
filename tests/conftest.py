from contextlib import asynccontextmanager

import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from src.infra.config import settings
from src.infra.gateways.database.setup import initialize_database


@pytest.fixture(scope="function")
@asynccontextmanager
async def initialize_database_fx() -> AsyncIOMotorClient:
    """Fixture that initializes the MongoDB database."""
    async with initialize_database(
        settings.DB_CONNECTION.get_secret_value(), settings.DB_NAME
    ) as db_client:
        try:
            yield db_client
        finally:
            await db_client.drop_database(settings.DB_NAME)

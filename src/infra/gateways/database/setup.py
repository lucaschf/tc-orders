"""Database.

This module configures and manages the connection to the MongoDB database and contains
the Beanie data models that represent the MongoDB collection documents.
Beanie models provide ORM functionality to simplify CRUD operations with the database.
"""

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

database_models = [
    # add beanie models here
]


async def initialize_database(db_uri: str, db_name: str) -> None:
    """Initialize the connection with MongoDB and Beanie for document models.

    This function performs the following actions:
     1. Establishes an asynchronous connection with MongoDB
        using the URI provided in the settings.
     2. Select the specified database from the settings.
     3. Initializes Beanie for the specified document models.
    This step is crucial for Beanie to operate correctly with MongoDB.

    Raises:
            ConnectionError: If the connection to MongoDB fails.
            RuntimeError: If the Beanie initialization fails or document models are not specified.
    """
    client = AsyncIOMotorClient(db_uri)
    database = client[db_name]

    # Beanie initialization
    await init_beanie(database, document_models=database_models)


__all__ = ["initialize_database"]

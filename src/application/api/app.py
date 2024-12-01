from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI

from src.infra.config import settings
from .exception_handlers import (
    domain_exception_handler,
    domain_validation_exception_handler,
    general_exception_handler,
)
from .middlewares import setup_cors
from .routers import register_routes
from ...domain.__shared.error import DomainError
from ...domain.__shared.validator import ValidationError as DomainValidationError
from ...infra.gateways.database.setup import initialize_database


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:  # noqa: RUF029, ARG001
    """Lifespan context manager for FastAPI application.

    This function defines the startup and shutdown logic for the FastAPI application.
    It connects to the database before the application starts receiving requests,
    and disconnects from the database after the application has finished handling requests.

    This ensures that the database connection is available for the
    entire lifespan of the application, and is properly cleaned up afterward.

    Args:
        _app (FastAPI): The FastAPI application instance.

    Yields:
        None: This context manager does not return any value.

    For more details, refer to the FastAPI documentation on Lifespan Events:
    https://fastapi.tiangolo.com/advanced/events/#lifespan-events
    """
    async with initialize_database(
        settings.DB_CONNECTION.get_secret_value(), settings.DB_NAME
    ):
        yield


app = FastAPI(
    docs_url=settings.DOCS_URL,
    redoc_url=settings.REDOC_URL,
    title=f"{settings.PROJECT_NAME} - {settings.ENVIRONMENT}",
    lifespan=lifespan,
)

register_routes(app)
setup_cors(app, settings.ALLOWED_ORIGINS)

app.add_exception_handler(DomainValidationError, domain_validation_exception_handler)
app.add_exception_handler(DomainError, domain_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

__all__ = ["app"]

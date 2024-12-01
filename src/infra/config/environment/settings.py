from pydantic import SecretStr
from pydantic_settings import BaseSettings

from .environment import Environment


class Settings(BaseSettings):
    """Singleton configuration class for application settings."""

    ENVIRONMENT: Environment = Environment.DEV
    """Specifies the current environment of the application."""

    DOCS_URL: str = "/docs"
    """The URL for the swagger documentation."""

    REDOC_URL: str = "/redoc"
    """The URL for the redoc documentation."""

    PROJECT_NAME: str = "TC - Fase 4"
    """The name of the project."""

    DB_CONNECTION: SecretStr
    """The connection string for the database."""

    DB_NAME: str
    """The name of the database."""


__all__ = ["Settings"]

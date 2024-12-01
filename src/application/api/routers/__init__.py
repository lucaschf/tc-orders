from fastapi import FastAPI

from .health_check_route import router as health_check_router


def register_routes(app: FastAPI) -> None:
    """Register all the routes for the FastAPI application.

    Args:
        app: The FastAPI application instance.
    """
    app.include_router(health_check_router)


__all__ = ["register_routes"]

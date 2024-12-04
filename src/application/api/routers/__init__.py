from fastapi import FastAPI

from .customer import customer_router
from .health_check_route import router as health_check_router
from .order import order_router


def register_routes(app: FastAPI) -> None:
    """Register all the routes for the FastAPI application.

    Args:
        app: The FastAPI application instance.
    """
    prefix = "/api/v1"

    app.include_router(health_check_router)
    app.include_router(customer_router, prefix=prefix)
    app.include_router(order_router, prefix=prefix)


__all__ = ["register_routes"]

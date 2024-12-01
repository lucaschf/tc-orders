from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthCheckOut(BaseModel):
    """Response model for health check."""

    status: str


@router.get(
    "/status",
    response_model=HealthCheckOut,
    tags=["Health Check"],
    description="Verifica o estado da API para garantir que ela está funcionando corretamente.",
)
def health_check() -> HealthCheckOut:
    """Check the health of the application.

    This endpoint returns a simple status indicating if the application is up and running.
    It can be used for monitoring purposes, by systems like Kubernetes, to check
    the health status of the application.

    Returns:
        HealthCheckOut: A model containing a status key with a value "OK".
    """
    return HealthCheckOut(status="OK")


__all__ = ["router"]

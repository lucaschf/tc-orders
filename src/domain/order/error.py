from dataclasses import dataclass

from src.domain.__shared.error import DomainError
from src.domain.order.order_status import OrderStatus


@dataclass(kw_only=True, frozen=True)
class InvalidStatusTransitionError(DomainError):
    """Raised when an invalid transition is attempted on a status."""

    status: OrderStatus
    new_status: OrderStatus
    message: str = "Invalid status transition"


__all__ = ["InvalidStatusTransitionError"]

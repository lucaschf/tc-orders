from dataclasses import dataclass

from src.domain.__shared.error import DomainError
from src.domain.order.order_status import OrderStatus


@dataclass(kw_only=True, frozen=True)
class InvalidStatusTransitionError(DomainError):
    """Raised when an invalid transition is attempted on a status."""

    status: OrderStatus
    new_status: OrderStatus
    message: str = "Invalid status transition"


@dataclass(kw_only=True, frozen=True)
class EmptyOrderError(DomainError):
    """Raised when an order is empty."""

    message: str = "Empty order"


__all__ = ["InvalidStatusTransitionError", "EmptyOrderError"]

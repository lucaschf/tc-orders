from dataclasses import dataclass
from datetime import datetime
from typing import Iterable

from src.domain.order import OrderStatus, Order


@dataclass(slots=True, frozen=True)
class CheckoutItemDTO:
    """CheckoutItem represents the data for an item in a checkout."""

    product_id: str
    quantity: int


@dataclass(slots=True, frozen=True)
class CheckoutOrderDTO:
    """CheckoutOrderRequest encapsulates all necessary data for performing a checkout."""

    customer_id: str
    items: Iterable[CheckoutItemDTO]


@dataclass
class CheckedOutItemDTO:
    """OrderItemResult represents the details of an order item."""

    product_id: str
    quantity: int
    unit_price: float


@dataclass(slots=True, frozen=True)
class CheckedOutOrderDTO:
    """OrderDetails represents the details of an order."""

    external_id: str
    created_at: datetime
    status: OrderStatus
    total_value: float
    items: Iterable[CheckedOutItemDTO]
    customer_id: str

    @classmethod
    def from_entity(cls: "CheckedOutOrderDTO", entity: Order) -> "CheckedOutOrderDTO":
        return cls(
            external_id=str(entity.external_id),
            created_at=entity.created_at,
            status=entity.status,
            total_value=entity.total_value,
            items=[
                CheckedOutItemDTO(
                    product_id=str(item.product_id),
                    quantity=item.quantity,
                    unit_price=item.unit_price,
                )
                for item in entity.items
            ],
            customer_id=str(entity.customer_id),
        )


__all__ = [
    "CheckoutItemDTO",
    "CheckoutOrderDTO",
    "CheckedOutItemDTO",
    "CheckedOutOrderDTO",
]

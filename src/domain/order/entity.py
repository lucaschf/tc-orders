from dataclasses import dataclass, field
from typing import List

from src.domain.__shared.entity import AggregateRoot
from src.domain.__shared.validator import ValidationResult
from src.domain.__shared.value_objects import UniqueEntityId
from src.domain.order.error import InvalidStatusTransitionError
from src.domain.order.order_item import OrderItem
from src.domain.order.order_status import OrderStatus
from src.domain.order.validator import OrderEntityValidatorFactory


@dataclass(kw_only=True)
class Order(AggregateRoot):
    """Represents an order in the system."""

    customer_id: UniqueEntityId
    items: List[OrderItem] = field(default_factory=list)
    total_value: float = field(default=0.0)
    status: OrderStatus = field(default_factory=lambda: OrderStatus.PAYMENT_PENDING)

    def __post_init__(self):
        super(Order, self).__post_init__()
        self.total_value = self.calculate_total()

    def add_item(self, item: OrderItem):
        self.items.append(item)
        self.total_value = self.calculate_total()

    def remove_item(self, item_id: UniqueEntityId):
        self.items = [item for item in self.items if item.id != item_id]
        self.total_value = self.calculate_total()

    def calculate_total(self) -> float:
        return sum(item.value * item.quantity for item in self.items)

    def update_status(self, new_status: OrderStatus) -> None:
        """Updates the status of the order.

        Args:
            new_status: The new status of the order.

        Raises:
            InvalidStatusTransitionError: If the new status is invalid.
        """
        if new_status not in self.status.get_allowed_transitions():
            raise InvalidStatusTransitionError(
                status=self.status, new_status=new_status
            )

        self.status = new_status

    def validate(self) -> ValidationResult:
        """Validates the order's attributes.

        This method checks if the user_uuid, products, and status are valid.
        If any of these conditions are not met,
         a DomainError will be raised with a relevant message.

        Raises:
            DomainError: If any of the order's attributes are invalid.
        """
        return OrderEntityValidatorFactory.create().validate(self)


__all__ = ["Order"]

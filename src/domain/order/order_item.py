from dataclasses import dataclass

from src.domain.__shared.entity import AggregateRoot
from src.domain.__shared.validator import ValidationResult
from src.domain.order.order_item_validator import OrderItemEntityValidatorFactory


@dataclass(kw_only=True)
class OrderItem(AggregateRoot):
    def validate(self) -> ValidationResult:
        return OrderItemEntityValidatorFactory.create().validate(self)

    product_id: str
    quantity: int
    value: float


__all__ = ["OrderItem"]

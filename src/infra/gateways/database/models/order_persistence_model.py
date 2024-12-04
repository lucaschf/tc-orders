from typing import Annotated, List

from beanie import Indexed, PydanticObjectId

from src.domain.__shared.value_objects import (
    ExternalEntityId,
    UniqueEntityId,
)
from src.domain.order import Order, OrderStatus
from src.domain.order.order_item import OrderItem
from src.infra.gateways.database.models.base import PersistenceModel


class OrderItemPersistenceModel(PersistenceModel[OrderItem]):
    product_id: str
    quantity: int
    value: float

    @staticmethod
    def from_entity(entity: OrderItem) -> "OrderItemPersistenceModel":
        return OrderItemPersistenceModel(
            product_id=entity.product_id,
            quantity=entity.quantity,
            value=entity.value,
            created_at=entity.created_at,
            external_id=str(
                entity.external_id,
            ),
        )

    def to_entity(self) -> OrderItem:
        return OrderItem(
            product_id=self.product_id,
            quantity=self.quantity,
            value=self.value,
            created_at=self.created_at,
            external_id=ExternalEntityId(str(self.external_id)),
        )


class OrderPersistenceModel(PersistenceModel[Order]):
    customer_id: Annotated[PydanticObjectId, Indexed]
    total_value: float
    status: OrderStatus
    items: List[OrderItemPersistenceModel]

    @staticmethod
    def from_entity(entity: Order) -> "OrderPersistenceModel":
        return OrderPersistenceModel(
            id=PydanticObjectId(entity.id.id) if entity.id else None,
            external_id=str(entity.external_id),
            created_at=entity.created_at,
            customer_id=PydanticObjectId(str(entity.customer_id)),
            total_value=entity.total_value,
            status=entity.status,
            items=[
                OrderItemPersistenceModel.from_entity(item) for item in entity.items
            ],
        )

    def to_entity(self) -> Order:
        return Order(
            _id=UniqueEntityId(str(self.id)) if self.id else None,
            external_id=ExternalEntityId(str(self.external_id)),
            created_at=self.created_at,
            customer_id=UniqueEntityId(str(self.customer_id)),
            total_value=self.total_value,
            status=self.status,
            items=[item.to_entity() for item in self.items],
        )

    class Settings:  # noqa: D106
        name = "customers"


__all__ = ["OrderPersistenceModel", "OrderItemPersistenceModel"]

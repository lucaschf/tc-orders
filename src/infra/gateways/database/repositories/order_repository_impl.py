from typing import Optional, List

from src.domain.__shared.error.repository_error import DuplicateKeyError
from src.domain.__shared.value_objects import (
    ExternalEntityId,
    UniqueEntityId,
)
from src.domain.order import Order
from src.domain.order.repository import IOrderRepository
from pymongo.errors import DuplicateKeyError as MongoDuplicateKeyError

from src.infra.gateways.database.models.order_persistence_model import (
    OrderPersistenceModel,
)


class MongoOrderRepository(IOrderRepository):
    """Repository for handling customer-related database operations."""

    async def list_all(self) -> List[Order]:
        found = await OrderPersistenceModel.all().to_list()
        return [order.to_entity() for order in found]

    async def insert(self, order: Order) -> Order:
        try:
            persisted = await OrderPersistenceModel.from_entity(order).insert()
            return persisted.to_entity()
        except MongoDuplicateKeyError as e:
            raise DuplicateKeyError(message=str(e)) from e

    async def find_by_id(self, identifier: str | UniqueEntityId) -> Optional[Order]:
        found = await OrderPersistenceModel.get(str(identifier))
        return found.to_entity() if found else None

    async def find_by_external_id(
        self, external_id: str | ExternalEntityId
    ) -> Optional[Order]:
        found = await OrderPersistenceModel.find_one({"external_id": str(external_id)})
        return found.to_entity() if found else None


__all__ = ["MongoOrderRepository"]

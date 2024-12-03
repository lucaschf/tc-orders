from datetime import datetime
from unittest.mock import patch, AsyncMock

import pytest
from beanie import PydanticObjectId

from src.domain.__shared.error.repository_error import DuplicateKeyError
from src.domain.__shared.value_objects import ExternalEntityId
from src.domain.order import OrderStatus, Order
from src.domain.order.order_item import OrderItem
from src.infra.gateways.database.models.order_persistence_model import (
    OrderPersistenceModel,
    OrderItemPersistenceModel,
)
from src.infra.gateways.database.repositories.order_repository_impl import (
    MongoOrderRepository,
)
from tests.__providers import UniqueEntityIdProvider
from pymongo.errors import DuplicateKeyError as MongoDuplicateKeyError


async def test_list_all_returns_orders(initialize_database_fx):
    async with initialize_database_fx:
        # noinspection PyArgumentList
        orders = [
            OrderPersistenceModel(
                id=PydanticObjectId(),
                external_id=str(ExternalEntityId()),
                customer_id=PydanticObjectId(),
                total_value=100.0,
                status=OrderStatus.PAYMENT_PENDING,
                items=[
                    OrderItemPersistenceModel(
                        product_id=PydanticObjectId(),
                        external_id=str(ExternalEntityId()),
                        quantity=1,
                        value=100.0,
                        created_at=datetime.now(),
                    )
                ],
                created_at=datetime.now(),
            ),
            OrderPersistenceModel(
                id=PydanticObjectId(),
                external_id=str(ExternalEntityId()),
                customer_id=PydanticObjectId(),
                total_value=200.0,
                status=OrderStatus.COMPLETED,
                items=[
                    OrderItemPersistenceModel(
                        product_id=PydanticObjectId(),
                        external_id=str(ExternalEntityId()),
                        quantity=1,
                        value=100.0,
                        created_at=datetime.now(),
                    )
                ],
                created_at=datetime.now(),
            ),
        ]

        with patch.object(
            OrderPersistenceModel,
            "all",
            return_value=AsyncMock(to_list=AsyncMock(return_value=orders)),
        ):
            repo = MongoOrderRepository()
            result = await repo.list_all()
            assert len(result) == len(orders)


async def test_insert_saves_order(initialize_database_fx):
    async with initialize_database_fx:
        order = Order(
            external_id=ExternalEntityId(),
            customer_id=UniqueEntityIdProvider.generate_unique_entity_id(),
            total_value=100.0,
            status=OrderStatus.PAYMENT_PENDING,
            items=[
                OrderItem(
                    external_id=ExternalEntityId(),
                    product_id=UniqueEntityIdProvider.generate_unique_entity_id(),
                    quantity=1,
                    value=100.0,
                )
            ],
        )

        persisted_order = OrderPersistenceModel.from_entity(order)

        with patch.object(
            OrderPersistenceModel,
            "insert",
            return_value=persisted_order,
        ):
            repo = MongoOrderRepository()
            result = await repo.insert(order)
            assert result == order


async def test_insert_raises_duplicate_key_error(initialize_database_fx):
    async with initialize_database_fx:
        order = Order(
            external_id=ExternalEntityId(),
            customer_id=UniqueEntityIdProvider.generate_unique_entity_id(),
            total_value=100.0,
            status=OrderStatus.PAYMENT_PENDING,
            items=[
                OrderItem(
                    external_id=ExternalEntityId(),
                    product_id=UniqueEntityIdProvider.generate_unique_entity_id(),
                    quantity=1,
                    value=100.0,
                )
            ],
        )

        with patch.object(
            OrderPersistenceModel,
            "insert",
            side_effect=MongoDuplicateKeyError(error="error"),
        ):
            repo = MongoOrderRepository()
            with pytest.raises(DuplicateKeyError):
                await repo.insert(order)


async def test_find_by_id_returns_order(initialize_database_fx):
    async with initialize_database_fx:
        order_id = UniqueEntityIdProvider.generate_unique_entity_id()
        found_order = OrderPersistenceModel.from_entity(
            Order(
                external_id=ExternalEntityId(),
                customer_id=UniqueEntityIdProvider.generate_unique_entity_id(),
                total_value=100.0,
                status=OrderStatus.PAYMENT_PENDING,
                items=[
                    OrderItem(
                        external_id=ExternalEntityId(),
                        product_id=UniqueEntityIdProvider.generate_unique_entity_id(),
                        quantity=1,
                        value=100.0,
                    )
                ],
            )
        )

        with patch.object(
            OrderPersistenceModel,
            "get",
            return_value=found_order,
        ):
            repo = MongoOrderRepository()
            result = await repo.find_by_id(order_id)
            assert result == found_order.to_entity()


async def test_find_by_id_returns_none(initialize_database_fx):
    async with initialize_database_fx:
        order_id = UniqueEntityIdProvider.generate_unique_entity_id()

        with patch.object(OrderPersistenceModel, "get", return_value=None):
            repo = MongoOrderRepository()
            result = await repo.find_by_id(order_id)
            assert result is None


async def test_find_by_external_id_returns_order(initialize_database_fx):
    async with initialize_database_fx:
        external_id = ExternalEntityId()

        found_order = OrderPersistenceModel.from_entity(
            Order(
                external_id=ExternalEntityId(),
                customer_id=UniqueEntityIdProvider.generate_unique_entity_id(),
                total_value=100.0,
                status=OrderStatus.PAYMENT_PENDING,
                items=[
                    OrderItem(
                        external_id=ExternalEntityId(),
                        product_id=UniqueEntityIdProvider.generate_unique_entity_id(),
                        quantity=1,
                        value=100.0,
                    )
                ],
            )
        )
        async_mock = AsyncMock(return_value=found_order)
        with patch.object(
            OrderPersistenceModel,
            "find_one",
            async_mock,
        ):
            repo = MongoOrderRepository()
            result = await repo.find_by_external_id(external_id)
            assert result == found_order.to_entity()


async def test_find_by_external_id_returns_none(initialize_database_fx):
    async with initialize_database_fx:
        external_id = ExternalEntityId()

        async_mock = AsyncMock(return_value=None)
        with patch.object(OrderPersistenceModel, "find_one", async_mock):
            repo = MongoOrderRepository()
            result = await repo.find_by_external_id(external_id)
            assert result is None

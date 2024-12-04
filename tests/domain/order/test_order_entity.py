import pytest

from src.domain.order import OrderStatus, InvalidStatusTransitionError
from src.domain.order.entity import Order
from src.domain.order.order_item import OrderItem
from tests.__providers import UniqueEntityIdProvider


def test_add_item_increases_total_value() -> None:
    order = Order(customer_id=UniqueEntityIdProvider.generate_unique_entity_id())
    item = OrderItem(
        product_id="1231312",
        quantity=2,
        value=50.0,
    )
    order.add_item(item)
    assert order.total_value == 100


def test_remove_item_decreases_total_value() -> None:
    order = Order(customer_id=UniqueEntityIdProvider.generate_unique_entity_id())
    item1 = OrderItem(
        _id=UniqueEntityIdProvider.generate_unique_entity_id(),
        product_id="1231312",
        quantity=2,
        value=50,
    )
    item2 = OrderItem(
        _id=UniqueEntityIdProvider.generate_unique_entity_id(),
        product_id="12313122",
        quantity=1,
        value=30,
    )
    order.add_item(item1)
    order.add_item(item2)
    order.remove_item(item1.id)
    assert order.total_value == 30


def test_calculate_total_returns_correct_value() -> None:
    order = Order(customer_id=UniqueEntityIdProvider.generate_unique_entity_id())
    item1 = OrderItem(
        product_id="1231312",
        quantity=2,
        value=50,
    )
    item2 = OrderItem(
        product_id="12313124",
        quantity=1,
        value=30,
    )
    order.add_item(item1)
    order.add_item(item2)
    assert order.calculate_total() == 130


def test_validate_order_with_valid_attributes() -> None:
    order = Order(customer_id=UniqueEntityIdProvider.generate_unique_entity_id())
    item = OrderItem(
        product_id="1231312",
        quantity=2,
        value=50,
    )
    order.add_item(item)
    validation_result = order.validate()
    assert validation_result.is_valid


def test_validate_order_with_invalid_attributes() -> None:
    order = Order(customer_id=UniqueEntityIdProvider.generate_unique_entity_id())
    item = OrderItem(
        product_id="1231312",
        quantity=-1,
        value=50,
    )
    order.add_item(item)
    validation_result = order.validate()
    assert not validation_result.is_valid


def test_update_status_changes_status_when_valid_transition() -> None:
    order = Order(customer_id=UniqueEntityIdProvider.generate_unique_entity_id())
    order.update_status(OrderStatus.RECEIVED)
    assert order.status == OrderStatus.RECEIVED


def test_update_status_raises_error_when_invalid_transition() -> None:
    order = Order(customer_id=UniqueEntityIdProvider.generate_unique_entity_id())
    with pytest.raises(InvalidStatusTransitionError):
        order.update_status(OrderStatus.COMPLETED)

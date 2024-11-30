from dataclasses import dataclass, replace
from datetime import datetime
from unittest.mock import patch

import pytest

from src.domain.__shared.entity import AggregateRoot
from src.domain.__shared.validator import (
    ValidationError,
    ValidationErrorDetails,
    ValidationResult,
)
from src.domain.__shared.value_objects import ExternalEntityId


@dataclass(slots=True)
class StubEntity(AggregateRoot):
    def validate(self) -> ValidationResult:  # noqa: D102
        return ValidationResult(is_valid=True)


def test_aggregate_root_creation() -> None:
    aggregate_root = StubEntity(_external_id=ExternalEntityId())
    assert aggregate_root.id is None
    assert isinstance(aggregate_root.external_id, ExternalEntityId)
    assert isinstance(aggregate_root.created_at, datetime)


def test_aggregate_root_validation_success() -> None:
    aggregate_root = StubEntity(_external_id=ExternalEntityId())
    aggregate_root.__post_init__()


def test_aggregate_root_validation_failure() -> None:
    class InvalidAggregateRoot(AggregateRoot):
        def validate(self) -> ValidationResult:
            return ValidationResult(
                is_valid=False,
                errors=[
                    ValidationErrorDetails(
                        msg="Validation error",
                        loc=("field",),
                    )
                ],
            )

    with pytest.raises(ValidationError):
        InvalidAggregateRoot()


def test_aggregate_root_calls_validate() -> None:
    with patch.object(StubEntity, "validate") as mock_validate:
        mock_validate.return_value = ValidationResult(is_valid=True)
        StubEntity()

    mock_validate.assert_called_once()


@dataclass(kw_only=True, slots=True)
class StubCustomerEntity(AggregateRoot):
    name: str

    def with_updated_name(self, new_name: str) -> "StubCustomerEntity":  # noqa: D102
        return replace(
            self,
            name=new_name,
        )

    def validate(self) -> ValidationResult:  # noqa: D102
        return ValidationResult(is_valid=True)


def test_set_method_set_for_existent_attribute() -> None:
    customer = StubCustomerEntity(name="John Doe")
    assert customer.name == "John Doe"

    customer = customer.with_updated_name("Jane Doe")
    assert customer.name == "Jane Doe"


def test_aggregate_root_accepts_empty_id() -> None:
    aggregate_root = StubEntity()
    assert aggregate_root.id is None


def test_aggregate_root_does_not_accepts_empty_external_id() -> None:
    with pytest.raises(ValidationError):
        StubEntity(_external_id=None)  # type: ignore


def test_aggregate_root_raises_exception_on_invalid_unique_id() -> None:
    with pytest.raises(ValidationError):
        StubEntity(_id=123)  # type: ignore


def test_aggregate_root_raises_exception_on_invalid_external_id() -> None:
    with pytest.raises(ValidationError):
        StubEntity(_external_id="invalid")  # type: ignore

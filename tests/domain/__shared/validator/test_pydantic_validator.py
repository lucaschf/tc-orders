import pytest
from pydantic import BaseModel, Field

from src.domain.__shared.validator import (
    IPydanticValidator,
    ValidationError,
)


class StubPydanticModel(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    age: int = Field(ge=0, le=120)


class StubValidator(IPydanticValidator):
    def get_pydantic_model(self) -> type[BaseModel]:  # noqa: D102
        return StubPydanticModel


@pytest.fixture
def validator() -> IPydanticValidator:
    return StubValidator()


def test_valid_data(validator: IPydanticValidator) -> None:
    data = {"name": "John Doe", "age": 30}
    result = validator.validate(data)

    assert result.is_valid
    assert result.errors == []


def test_invalid_data(validator: IPydanticValidator) -> None:
    data = {"name": "Jo", "age": 150}
    result = validator.validate(data)

    assert not result.is_valid
    assert len(result.errors) == 2

    expected_errors = {
        ("name",): "String should have at least 3 characters",
        ("age",): "Input should be less than or equal to 120",
    }

    for loc, msg in expected_errors.items():
        error = next((e for e in result.errors if e.loc == loc), None)
        assert error is not None
        assert error.msg == msg


def test_invalid_input_type(validator: IPydanticValidator) -> None:
    data = "invalid data"
    result = validator.validate(data)

    assert not result.is_valid
    assert len(result.errors) == 1

    error = result.errors[0]
    assert error.loc == ()
    assert (
        error.msg
        == "Input should be a valid dictionary or object to extract fields from"
    )


def test_validate_or_raise_valid(validator: IPydanticValidator) -> None:
    data = {"name": "Alice", "age": 25}
    validator.validate_or_raise(data)


def test_validate_or_raise_invalid(validator: IPydanticValidator) -> None:
    data = {"name": "", "age": -1}
    with pytest.raises(ValidationError) as exc_info:
        validator.validate_or_raise(data)

    assert len(exc_info.value.errors) == 2

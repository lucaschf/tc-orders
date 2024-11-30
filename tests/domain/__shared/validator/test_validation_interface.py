import pytest

from src.domain.__shared.validator import (
    IValidator,
    ValidationError,
    ValidationErrorDetails,
    ValidationResult,
)


def test_raise_error_when_validate_is_not_implemented() -> None:
    with pytest.raises(TypeError) as ex:
        IValidator()

    assert str(ex.value) == (
        "Can't instantiate abstract class IValidator without an"
        " implementation for abstract method 'validate'"
    )


class PositiveNumberValidatorStub(IValidator[int]):
    def validate(self, obj: int) -> ValidationResult:  # noqa: D102
        if obj < 0:
            return ValidationResult(
                is_valid=False,
                errors=[
                    ValidationErrorDetails(
                        msg="Value must be non-negative",
                        loc=("obj",),
                    )
                ],
            )

        return ValidationResult(is_valid=True)


def test_validate_success() -> None:
    validator = PositiveNumberValidatorStub()
    result = validator.validate(5)
    assert result.is_valid
    assert result.errors == []


def test_validate_failure() -> None:
    validator = PositiveNumberValidatorStub()
    result = validator.validate(-3)
    assert not result.is_valid
    assert len(result.errors) == 1
    assert result.errors[0].msg == "Value must be non-negative"
    assert result.errors[0].loc == ("obj",)


def test_do_not_raises_when_validate_or_raise_is_called() -> None:
    validator = PositiveNumberValidatorStub()
    try:
        validator.validate_or_raise(10)
    except ValidationError:
        pytest.fail("ValidationError raised unexpectedly")


def test_raises_when_validate_or_raise_is_called() -> None:
    validator = PositiveNumberValidatorStub()
    with pytest.raises(ValidationError) as exc_info:
        validator.validate_or_raise(-1)

    assert exc_info.value.message == "Validation error"
    errors = exc_info.value.errors

    assert len(errors) == 1
    errors = list(errors)
    assert errors[0].msg == "Value must be non-negative"
    assert errors[0].loc == ("obj",)

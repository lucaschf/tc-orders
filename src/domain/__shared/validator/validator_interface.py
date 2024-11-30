from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List

from src.domain.__shared.validator import ValidationErrorDetails
from src.domain.__shared.validator.error import ValidationError


@dataclass(slots=True)
class ValidationResult:
    """A class that represents the result of a validation operation.

    Attributes:
        is_valid: Indicates whether the validation was successful.
        errors: A list of validation errors, if any.
    """

    is_valid: bool
    errors: List[ValidationErrorDetails] = field(default_factory=list)


class IValidator[T](ABC):
    """An interface for validators."""

    @abstractmethod
    def validate(self, obj: T) -> ValidationResult:
        """Validates the provided object against the defined validation rules.

        Args:
            obj (T): The object to be validated.

        Returns:
            ValidationResult: The result of the validation operation.
        """

    def validate_or_raise(self, obj: T) -> None:
        """Validates the object and throws ValidationError if it fails.

        Args:
            obj (T): The object to be validated.

        Raises:
            ValidationError: If the validation fails.
        """
        validation_result = self.validate(obj)
        if not validation_result.is_valid:
            raise ValidationError(errors=validation_result.errors)


__all__ = ["IValidator", "ValidationResult"]

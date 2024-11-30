from dataclasses import dataclass, field
from typing import List

from src.domain.__shared.error import DomainError
from src.domain.__shared.validator.error_details import ValidationErrorDetails


@dataclass(kw_only=True, frozen=True, slots=True)
class ValidationError(DomainError):
    """A class representing a validation error."""

    message: str = "Validation error"
    errors: List[ValidationErrorDetails] = field(default_factory=list)

    def __repr__(self) -> str:
        errors_count = len(self.errors)
        errors_as_str = ", ".join([f"{error!r}" for error in self.errors])
        return f"{errors_count} Validation error{'s' if errors_count > 1 else ''}: {errors_as_str}"


__all__ = ["ValidationError"]

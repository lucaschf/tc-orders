from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from ..validator import ValidationError, ValidationErrorDetails
from ..validator.validator_interface import ValidationResult
from ..value_objects import ExternalEntityId, UniqueEntityId


@dataclass(kw_only=True, slots=True)
class AggregateRoot(ABC):
    """Base class for aggregate roots.

    Attributes:
        _id: The unique identifier for the aggregate root.
        external_id: The external identifier for the aggregate root.
        created_at: The timestamp when the aggregate root was created.
    """

    _id: Optional[UniqueEntityId] = None
    external_id: ExternalEntityId = field(default_factory=ExternalEntityId)
    created_at: datetime = field(default_factory=datetime.now)

    @property
    def id(self) -> Optional[UniqueEntityId]:
        """Property to get the unique identifier."""
        return self._id

    @abstractmethod
    def validate(self) -> ValidationResult:
        """Validate the aggregate root.

        Raises:
            ValidationError: If the validation fails.
        """

    def __post_init__(self) -> None:
        """Post-initialization processing to validate the aggregate root."""
        validation_result = self.validate()

        additional_validations = [
            self._validate_created_at(),
            self._validate_id(),
            self._validate_external_id(),
        ]

        for v in additional_validations:
            validation_result.errors.extend(v.errors)
            if not v.is_valid:
                validation_result.is_valid = False

        if not validation_result.is_valid:
            raise ValidationError(errors=validation_result.errors)

    def _validate_created_at(self) -> ValidationResult:
        """Validates the unique identifier.

        Returns:
            ValidationResult: The result of the validation operation.
        """
        if not isinstance(self.created_at, datetime):
            return ValidationResult(
                is_valid=False,
                errors=[
                    ValidationErrorDetails(
                        loc=("created_at",),
                        msg="The created_at field must be a datetime object.",
                    )
                ],
            )
        return ValidationResult(is_valid=True)

    def _validate_id(self) -> ValidationResult:
        """Validates the unique identifier.

        Returns:
            ValidationResult: The result of the validation operation.
        """
        # If the id is not set, we assume that it is a new entity, and we don't need to validate it
        if not self.id or type(self.id) is UniqueEntityId:
            return ValidationResult(is_valid=True)

        return ValidationResult(
            is_valid=False,
            errors=[
                ValidationErrorDetails(
                    loc=("id",),
                    msg="The id field must be a UniqueEntityId object.",
                )
            ],
        )

    def _validate_external_id(self) -> ValidationResult:
        """Validates the external identifier.

        Returns:
            ValidationResult: The result of the validation operation.
        """
        if isinstance(self.external_id, ExternalEntityId):
            return ValidationResult(is_valid=True)

        return ValidationResult(
            is_valid=False,
            errors=[
                ValidationErrorDetails(
                    loc=("external_id",),
                    msg="The external_id field must be an ExternalEntityId object.",
                )
            ],
        )


__all__ = ["AggregateRoot"]

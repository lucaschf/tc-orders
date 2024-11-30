from typing import Any

from bson import ObjectId

from src.domain.__shared.validator import IValidator, ValidationErrorDetails, ValidationResult


class ObjectIdValidator(IValidator[str]):
    def validate(self, value: Any) -> ValidationResult:  # noqa: ANN401
        if not isinstance(value, (str, ObjectId)):
            return ValidationResult(
                is_valid=False,
                errors=[
                    ValidationErrorDetails(
                        loc=("id",),
                        msg="ID inválido",
                    )
                ],
            )

        if not ObjectId.is_valid(value):
            return ValidationResult(
                is_valid=False,
                errors=[
                    ValidationErrorDetails(
                        loc=("id",),
                        msg="ID inválido",
                    )
                ],
            )

        return ValidationResult(is_valid=True)


class UniqueEntityIdValidatorFactory:
    """A factory class responsible for creating validators for UniqueEntityIds.

    This factory provides a centralized point for getting concrete validator
    implementations, adhering to the Dependency Inversion Principle.
    """

    @staticmethod
    def create() -> IValidator[str]:
        """Creates and returns a concrete validator for UniqueEntityIds.

        Returns:
            IValidator[str]:An instance of the validator for validating UniqueEntityIds.
        """
        return ObjectIdValidator()


__all__ = ["UniqueEntityIdValidatorFactory"]

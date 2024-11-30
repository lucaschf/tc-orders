from typing import Type

from pydantic import BaseModel, EmailStr

from src.domain.__shared.validator import IPydanticValidator, IValidator


class EmailAddressValidationRule(BaseModel):
    """A Pydantic model that represents a validation rule for an EmailAddress value object.

    This class is responsible for defining the rules that will be used to
    validate an email address.
    """

    address: EmailStr


class EmailAddressValidator(IPydanticValidator):
    """A validator for EmailAddress value objects."""

    def get_pydantic_model(self) -> Type[BaseModel]:
        """Gets the Pydantic model used for validation."""
        return EmailAddressValidationRule


class EmailAddressValidatorFactory:
    """A factory class for creating instances of EmailAddressValidator."""

    @staticmethod
    def create() -> IValidator:
        """Creates a new instance of EmailAddressValidator."""
        return EmailAddressValidator()


__all__ = ["EmailAddressValidatorFactory"]

from typing import Type

from pydantic import BaseModel, ConfigDict, Field

from src.domain.__shared.validator import IValidator
from src.domain.__shared.validator.pydantic_validator import (
    IPydanticValidator,
)
from src.domain.__shared.value_objects import EmailAddress, CPF


# noinspection PyNestedDecorators
class CustomerValidationRule(BaseModel):
    """A Pydantic model that represents a validation rule for a User entity.

    This class is responsible for defining the rules that will be used to
    validate a User entity.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, str_strip_whitespace=True)

    name: str = Field(min_length=3, max_length=150)
    email: EmailAddress
    cpf: CPF


class CustomerEntityValidator(IPydanticValidator):
    """A concrete implementation of a validator for Customer entities.

    This class is responsible for validating User entities based on a set of
    predefined rules.
    """

    def get_pydantic_model(self) -> Type[BaseModel]:
        """Gets the Pydantic model used for validation."""
        return CustomerValidationRule


class CustomerEntityValidatorFactory:
    """A factory class responsible for creating validators for User entities.

    This factory provides a centralized point for getting concrete validator
    implementations, adhering to the Dependency Inversion Principle.
    """

    @staticmethod
    def create() -> IValidator:
        """Creates and returns a concrete validator for user entities.

        Returns:
            IValidator[User]:An instance Validator for validating user entity.
        """
        return CustomerEntityValidator()


__all__ = ["CustomerEntityValidator"]

from typing import Type

from pydantic import BaseModel, ConfigDict

from src.domain.__shared.validator import IValidator
from src.domain.__shared.validator.pydantic_validator import (
    IPydanticValidator,
)


class OrderItemValidationRule(BaseModel):
    """A Pydantic model that represents a validation rule for an OrderItem entity.

    This class is responsible for defining the rules that will be used to
    validate an OrderItem entity.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    product_id: str
    quantity: int
    value: float


class OrderItemEntityValidator(IPydanticValidator):
    """A concrete implementation of a validator for OrderItem entities.

    This class is responsible for validating order item entities based on a set of
    predefined rules.
    """

    def get_pydantic_model(self) -> Type[BaseModel]:
        """Gets the Pydantic model used for validation."""
        return OrderItemValidationRule


class OrderItemEntityValidatorFactory:
    """A factory class responsible for creating validators for order item entities.

    This factory provides a centralized point for getting concrete validator
    implementations, adhering to the Dependency Inversion Principle.
    """

    @staticmethod
    def create() -> IValidator:
        """Creates and returns a concrete validator for order item entities.

        Returns:
            IValidator[OrderItem]:An instance Validator for validating order item entity.
        """
        return OrderItemEntityValidator()


__all__ = ["OrderItemEntityValidatorFactory"]

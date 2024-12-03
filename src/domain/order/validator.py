from typing import Type, List

from pydantic import BaseModel, ConfigDict, Field

from src.domain.__shared.validator import IValidator
from src.domain.__shared.validator.pydantic_validator import (
    IPydanticValidator,
)
from src.domain.__shared.value_objects import UniqueEntityId
from src.domain.order.order_item import OrderItem
from src.domain.order.order_status import OrderStatus


# noinspection PyNestedDecorators
class OrderValidationRule(BaseModel):
    """A Pydantic model that represents a validation rule for an Order entity.

    This class is responsible for defining the rules that will be used to
    validate an Order entity.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    customer_id: UniqueEntityId
    items: List[OrderItem]
    total_value: float = Field(ge=0.0)
    status: OrderStatus


class OrderEntityValidator(IPydanticValidator):
    """A concrete implementation of a validator for Order entities.

    This class is responsible for validating order entities based on a set of
    predefined rules.
    """

    def get_pydantic_model(self) -> Type[BaseModel]:
        """Gets the Pydantic model used for validation."""
        return OrderValidationRule


class OrderEntityValidatorFactory:
    """A factory class responsible for creating validators for order entities.

    This factory provides a centralized point for getting concrete validator
    implementations, adhering to the Dependency Inversion Principle.
    """

    @staticmethod
    def create() -> IValidator:
        """Creates and returns a concrete validator for order entities.

        Returns:
            IValidator[Order]:An instance Validator for validating order entity.
        """
        return OrderEntityValidator()


__all__ = ["OrderEntityValidatorFactory"]

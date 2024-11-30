from dataclasses import dataclass, field

from src.domain.__shared.entity import AggregateRoot
from src.domain.__shared.validator import ValidationResult
from src.domain.__shared.value_objects import CPF, EmailAddress
from src.domain.customer.validator import CustomerEntityValidatorFactory


@dataclass(kw_only=True, slots=True, frozen=True)
class Customer(AggregateRoot):
    """Represents a customer in the system.

    Attributes:
    name: The customer's name.
    cpf: The customer's CPF.
    email: The customer's email.
    """

    name: str = field()
    cpf: CPF = field()
    email: EmailAddress = field()

    def validate(self) -> ValidationResult:
        """Validates the customer's attributes.

        This method checks if the customer's name, CPF, and email are not null or empty.
        If any of these conditions are not met, a DomainError will be raised
        with a relevant message.

        Raises:
           DomainError: If any of the customer's attributes are null or empty.
        """
        return CustomerEntityValidatorFactory.create().validate(self)


__all__ = ["Customer"]

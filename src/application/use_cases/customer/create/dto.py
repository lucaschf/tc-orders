from dataclasses import dataclass
from datetime import datetime

from src.domain.__shared.value_objects import EmailAddress, CPF


@dataclass
class CustomerCreationDTO:
    """Data structure for holding customer creation data.

    Attributes:
        name: The name of the customer.
        cpf: The CPF (Cadastro de Pessoas Físicas) of the customer.
        email: The email address of the customer.
    """

    name: str
    cpf: CPF
    email: EmailAddress


@dataclass
class CustomerCreatedDTO:
    """Data structure for holding data of a customer.

    Attributes:
        name: The name of the customer.
        cpf: The CPF of the customer.
        email: The email address of the customer.
        external_id: The unique identifier of the customer.
        created_at: The timestamp when the customer was created.
    """

    name: str
    cpf: CPF
    email: EmailAddress
    external_id: str
    created_at: datetime


__all__ = [
    "CustomerCreationDTO",
    "CustomerCreatedDTO",
]

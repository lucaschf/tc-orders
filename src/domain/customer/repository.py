from abc import ABC, abstractmethod

from src.domain.__shared.interfaces import IRepository
from src.domain.__shared.value_objects import CPF, EmailAddress
from src.domain.customer import Customer


class ICustomerRepository(IRepository[Customer], ABC):
    """Repository for handling customer persistence."""

    @abstractmethod
    async def find(
        self, cpf: CPF | None, email: EmailAddress | None
    ) -> Customer | None:
        """Check if a customer already exists in the database either by cpf, email or both.

        Args:
            cpf: The customer's CPF.
            email: The customer's email.

        Returns:
            bool: True if the customer exists, False otherwise.
        """

    async def get_by_cpf(self, cpf: CPF) -> Customer | None:
        """Get a customer by their CPF.

        Args:
            cpf: The customer's CPF.

        Returns:
            Customer: The customer data if found, None otherwise.
        """
        return await self.find(cpf=cpf, email=None)


__all__ = ["ICustomerRepository"]

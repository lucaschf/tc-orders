from src.application.use_cases.customer.create.dto import (
    CustomerCreationDTO,
    CustomerCreatedDTO,
)
from src.domain.__shared.error import DomainError
from src.domain.__shared.error.repository_error import DuplicateKeyError
from src.domain.customer import Customer
from src.domain.customer.repository import ICustomerRepository


class CreateCustomerUseCase:
    """A use case for creating a new customer."""

    def __init__(self, customer_repository: ICustomerRepository) -> None:
        self.customer_repository = customer_repository

    async def execute(self, customer_data: CustomerCreationDTO) -> CustomerCreatedDTO:
        """Creates a new customer using the provided data and adds it to the repository.

        Args:
            customer_data: The data for creating the new customer.

        Returns:
            Customer: The newly created customer.

        Raises:
            DomainError: If the customer already exists.
        """
        customer = Customer(
            name=customer_data.name, cpf=customer_data.cpf, email=customer_data.email
        )

        try:
            db_customer = await self.customer_repository.insert(customer)
        except DuplicateKeyError as e:
            raise DomainError(message="Customer already exists") from e

        return CustomerCreatedDTO(
            name=db_customer.name,
            cpf=db_customer.cpf,
            email=db_customer.email,
            created_at=db_customer.created_at,
            external_id=str(db_customer.external_id),
        )


__all__ = ["CreateCustomerUseCase"]

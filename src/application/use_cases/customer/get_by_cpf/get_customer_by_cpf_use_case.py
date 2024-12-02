from src.application.use_cases.customer.error import CustomerNotFoundError
from src.application.use_cases.customer.get_by_cpf.dto import CustomerDTO
from src.domain.__shared.value_objects import CPF
from src.domain.customer import ICustomerRepository


class GetCustomerByCpfUseCase:
    """A use case for getting a customer by their CPF."""

    def __init__(self, customer_repository: ICustomerRepository) -> None:
        self.customer_repository = customer_repository

    async def execute(self, cpf: str) -> CustomerDTO:
        """Get a customer by their CPF.

        Args:
            cpf: The customer's CPF.

        Returns:
            Customer: The customer data if found.

        Raises:
            CustomerNotFoundError: If the customer is not found.
        """
        customer = await self.customer_repository.get_by_cpf(CPF(number=cpf))

        if not customer:
            raise CustomerNotFoundError(
                search_params={"cpf": cpf}, message="Customer not found"
            )

        return CustomerDTO(
            name=customer.name,
            cpf=customer.cpf,
            email=customer.email,
            created_at=customer.created_at,
            external_id=str(customer.external_id),
        )


__all__ = ["GetCustomerByCpfUseCase"]

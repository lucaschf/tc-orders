from injector import Module, inject, provider, singleton

from src.application.use_cases.customer.create import CreateCustomerUseCase
from src.application.use_cases.customer.get_by_cpf import GetCustomerByCpfUseCase
from src.domain.customer import ICustomerRepository
from src.infra.gateways.database.repositories import MongoCustomerRepository


class CustomerModule(Module):
    """Dependency injection module for the Role domain."""

    @singleton
    @provider
    def provide_customer_repository(self) -> ICustomerRepository:
        """Provide the customer repository."""
        return MongoCustomerRepository()

    @provider
    @inject
    def provide_create_customer_use_case(
        self, customer_repository: ICustomerRepository
    ) -> CreateCustomerUseCase:
        """Provide the creation customer use case."""
        return CreateCustomerUseCase(customer_repository=customer_repository)

    @provider
    @inject
    def provide_get_customer_by_cpf_use_case(
        self, customer_repository: ICustomerRepository
    ) -> GetCustomerByCpfUseCase:
        """Provide the get customer use case."""
        return GetCustomerByCpfUseCase(customer_repository=customer_repository)


__all__ = ["CustomerModule"]

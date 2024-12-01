from injector import Module, inject, provider, singleton

from src.application.use_cases.customer.create import CreateCustomerUseCase
from src.domain.customer import ICustomerRepository
from src.infra.gateways.database.repositories import MongoCustomerRepository


class CustomerModule(Module):
    """Dependency injection module for the Role domain."""

    @singleton
    @provider
    def provide_customer_repository(self) -> ICustomerRepository:
        """Provide the role repository."""
        return MongoCustomerRepository()

    @provider
    @inject
    def provide_create_customer_use_case(
        self, customer_repository: ICustomerRepository
    ) -> CreateCustomerUseCase:
        """Provide the creation role use case."""
        return CreateCustomerUseCase(customer_repository=customer_repository)


__all__ = ["CustomerModule"]

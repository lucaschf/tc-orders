from injector import Module, inject, provider, singleton

from src.application.use_cases.order.checkout.checkout import CheckoutUseCase
from src.domain.__shared.interfaces import IProductService
from src.domain.customer import ICustomerRepository
from src.domain.order.repository import IOrderRepository
from src.infra.gateways.database.repositories.order_repository_impl import (
    MongoOrderRepository,
)


class OrderModule(Module):
    """Dependency injection module for the Order domain."""

    @singleton
    @provider
    def provide_order_repository(self) -> IOrderRepository:
        """Provide the order repository."""
        return MongoOrderRepository()

    @provider
    @inject
    def provide_checkout_use_case(
        self,
        order_repository: IOrderRepository,
        customer_repository: ICustomerRepository,
        product_service: IProductService,
    ) -> CheckoutUseCase:
        """Provide the checkout use case."""
        return CheckoutUseCase(
            order_repository=order_repository,
            customer_repository=customer_repository,
            product_service=product_service,
        )


__all__ = ["OrderModule"]

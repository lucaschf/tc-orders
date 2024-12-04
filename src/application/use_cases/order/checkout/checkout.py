from typing import Iterable, List, Dict

from src.application.use_cases.order.checkout.dto import (
    CheckoutOrderDTO,
    CheckedOutOrderDTO,
    CheckoutItemDTO,
)
from src.domain.__shared.interfaces import IProductService
from src.domain.__shared.interfaces.product_service import Product
from src.domain.customer import ICustomerRepository, Customer
from src.domain.customer_error import CustomerNotFoundError
from src.domain.order import Order
from src.domain.order.error import EmptyOrderError
from src.domain.order.order_item import OrderItem
from src.domain.order.repository import IOrderRepository


class CheckoutUseCase:
    """CheckoutUseCase encapsulates the business logic for creating orders."""

    def __init__(
        self,
        order_repository: IOrderRepository,
        customer_repository: ICustomerRepository,
        product_service: IProductService,
    ) -> None:
        """Initializes a new instance of the CheckoutUseCase class.

        Args:
            order_repository: The repository instance for order persistence operations.
            customer_repository: The repository instance for customer persistence operations.
            product_service: The service for product operations.
        """

        self._order_repository = order_repository
        self._customer_repository = customer_repository
        self._product_service = product_service

    async def checkout(self, request: CheckoutOrderDTO) -> CheckedOutOrderDTO:
        """Creates a new order in the system.

        Args:
            request: The checkout request data.

        Returns:
            CheckoutResponse: The response containing the order number.

        Raises:
            EmptyOrderError: If the order has no items.
            OrderCreationFailedDueToMissingProductsError: If any product is not found.
            CustomerNotFoundError: If the customer is not found.
        """
        if not request.items:
            raise EmptyOrderError()

        customer = await self._get_customer(request.customer_id)
        product_map = self._product_service.fetch_products_by_ids(
            [item.product_id for item in request.items]
        )

        order_items = self._create_order_items(request.items, product_map)
        order = Order(customer_id=customer.id, items=list(order_items))
        created_order = await self._order_repository.insert(order)

        # TODO: Implement order production and payment request

        return CheckedOutOrderDTO.from_entity(created_order)

    async def _get_customer(self, customer_external_id: str) -> Customer:
        """Gets a customer by external id.

        Args:
            customer_external_id: The customer's external identifier.

        Returns:
            Customer: The customer entity if found.

        Raises:
            CustomerNotFoundError: If the customer is not found.
        """
        customer = await self._customer_repository.find_by_external_id(
            customer_external_id
        )
        if not customer:
            raise CustomerNotFoundError(
                search_params={"external_id": customer_external_id}
            )

        return customer

    @staticmethod
    def _create_order_items(
        checkout_items: Iterable[CheckoutItemDTO], products: List[Product]
    ) -> Iterable[OrderItem]:
        product_map: Dict[str, Product] = {product.id: product for product in products}

        order_items: List[OrderItem] = []

        for checkout_item in checkout_items:
            if product := product_map.get(checkout_item.product_id):
                order_items.append(
                    OrderItem(
                        product_id=checkout_item.product_id,
                        quantity=checkout_item.quantity,
                        value=product.price,
                    )
                )
            else:
                raise ValueError(
                    f"Product with ID {checkout_item.product_id} not found."
                )

        return order_items


__all__ = ["CheckoutUseCase"]

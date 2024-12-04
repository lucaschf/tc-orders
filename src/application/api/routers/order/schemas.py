from typing import List

from pydantic import BaseModel, Field

from src.application.api.types import PydanticExternalEntityId
from src.application.use_cases.order.checkout.dto import (
    CheckoutOrderDTO,
    CheckoutItemDTO,
)


class OrderItemIn(BaseModel):
    """Schema for creating a new order product."""

    quantity: int = Field(description="The quantity of the product", gt=0)
    product_id: str = Field(description="The product id")


class OrderIn(BaseModel):
    """Schema for creating a new order."""

    customer_id: PydanticExternalEntityId = Field(description="The customer identifier")
    items: List[OrderItemIn] = Field(description="List of products in the order")

    def to_checkout_request(self) -> CheckoutOrderDTO:
        """Converts the OrderIn instance to a CheckoutRequest instance."""
        return CheckoutOrderDTO(
            customer_id=self.customer_id,
            items=[
                CheckoutItemDTO(product_id=item.product_id, quantity=item.quantity)
                for item in self.items
            ],
        )


class OrderCreationOut(BaseModel):
    """Schema for returning the result of creating an order."""

    external_id: PydanticExternalEntityId = Field(description="The order number")


__all__ = ["OrderCreationOut", "OrderIn", "OrderItemIn"]

from http import HTTPStatus

from fastapi import APIRouter, Depends

from src.application.api.routers.order.schemas import OrderIn, OrderCreationOut
from src.application.di import dependency_injector
from src.application.use_cases.order.checkout.checkout import CheckoutUseCase

router = APIRouter(tags=["Order"], prefix="/orders")


@router.post(
    "/checkout", response_model=OrderCreationOut, status_code=HTTPStatus.CREATED
)
async def checkout(
    order_in: OrderIn,
    checkout_use_case: CheckoutUseCase = Depends(
        lambda: dependency_injector.get(CheckoutUseCase)
    ),
    # noqa: B008
) -> OrderCreationOut:
    """Process a fake checkout by adding selected products to the order queue."""
    order = await checkout_use_case.checkout(order_in)
    return OrderCreationOut.model_validate(order, from_attributes=True)


__all__ = ["router"]

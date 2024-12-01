from http import HTTPStatus

from fastapi import APIRouter, Depends, Response

from src.application.api.routers.customer.schemas import (
    CustomerCreationIn,
    CustomerDetailsOut,
)
from src.application.api.schemas import HttpErrorOut
from src.application.di import dependency_injector
from src.application.use_cases.customer.create import CreateCustomerUseCase

router = APIRouter(tags=["Customer"], prefix="/customer")


@router.post(
    "/",
    status_code=HTTPStatus.CREATED,
    responses={400: {"model": HttpErrorOut}},
    description="Creates a new customer in the system. Accepts a request body with the customer's "
    "name, CPF, and email.",
)
async def create_customer(
    response: Response,
    inputs: CustomerCreationIn,
    create_customer_use_case: CreateCustomerUseCase = Depends(
        lambda: dependency_injector.get(CreateCustomerUseCase)
    ),
) -> CustomerDetailsOut:
    customer = await create_customer_use_case.execute(
        inputs.to_customer_creation_data()
    )
    response.headers["Location"] = f"{router.prefix}/{customer.cpf}"
    return CustomerDetailsOut.from_dto(customer)


__all__ = ["router"]

from http import HTTPStatus

from fastapi import APIRouter, Depends, Response

from src.application.api.routers.customer.schemas import (
    CustomerCreationIn,
    CustomerDetailsOut,
)
from src.application.api.schemas import HttpErrorOut
from src.application.api.types import CPFStr
from src.application.di import dependency_injector
from src.application.use_cases.customer.create import CreateCustomerUseCase
from src.application.use_cases.customer.get_by_cpf import GetCustomerByCpfUseCase

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


@router.get(
    "/{cpf}",
    responses={404: {"model": HttpErrorOut}, 400: {"model": HttpErrorOut}},
    description="Retrieves a customer from the system using their CPF. The CPF is passed as a path "
    "parameter.",
)
async def get_by_cpf(
    cpf: CPFStr,
    get_customer_use_case: GetCustomerByCpfUseCase = Depends(  # noqa: B008
        lambda: dependency_injector.get(GetCustomerByCpfUseCase)
    ),
) -> CustomerDetailsOut:
    customer = await get_customer_use_case.execute(cpf)
    return CustomerDetailsOut.from_dto(customer)


__all__ = ["router"]

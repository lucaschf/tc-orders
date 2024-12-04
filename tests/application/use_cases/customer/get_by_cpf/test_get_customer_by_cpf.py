from datetime import datetime

import pytest
from unittest.mock import AsyncMock
from src.application.use_cases.customer.get_by_cpf.get_customer_by_cpf_use_case import (
    GetCustomerByCpfUseCase,
)
from src.application.use_cases.customer.get_by_cpf.dto import CustomerDTO
from src.domain.__shared.value_objects import CPF, EmailAddress
from src.domain.customer import Customer, ICustomerRepository
from src.domain.customer_error import CustomerNotFoundError
from tests.__providers import UniqueEntityIdProvider


async def test_execute_returns_customer_dto_when_customer_found():
    customer = Customer(
        _id=UniqueEntityIdProvider().generate_unique_entity_id(),
        name="John Doe",
        email=EmailAddress(address="some@example.com"),
        cpf=CPF(number="10856446696"),
        created_at=datetime.now(),
    )
    mock_repository = AsyncMock(ICustomerRepository)
    mock_repository.get_by_cpf.return_value = customer

    use_case = GetCustomerByCpfUseCase(customer_repository=mock_repository)
    result = await use_case.execute(cpf="10856446696")

    assert result == CustomerDTO(
        name="John Doe",
        cpf=customer.cpf,
        email=customer.email,
        created_at=customer.created_at,
        external_id=str(customer.external_id),
    )


async def test_execute_raises_customer_not_found_error_when_customer_not_found():
    mock_repository = AsyncMock(ICustomerRepository)
    mock_repository.get_by_cpf.return_value = None

    use_case = GetCustomerByCpfUseCase(customer_repository=mock_repository)

    with pytest.raises(
        CustomerNotFoundError, match="{'cpf': '10856446696'}"
    ) as exc_info:
        await use_case.execute(cpf="10856446696")

    assert exc_info.value.message == "Customer not found"

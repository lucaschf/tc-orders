from datetime import datetime
from unittest.mock import Mock

import pytest

from src.application.use_cases.customer.create.create import CreateCustomerUseCase
from src.application.use_cases.customer.create.dto import CustomerCreationDTO
from src.domain.__shared.error import DomainError
from src.domain.__shared.error.repository_error import DuplicateKeyError
from src.domain.__shared.validator import ValidationError
from src.domain.__shared.value_objects import EmailAddress, CPF, ExternalEntityId
from src.domain.customer import Customer
from src.domain.customer.repository import ICustomerRepository


async def test_create_customer_success() -> None:
    customer_repository_mock = Mock(spec=ICustomerRepository)
    create_customer_use_case_fx = CreateCustomerUseCase(customer_repository_mock)

    customer_repository_mock.find.return_value = None
    customer_data = CustomerCreationDTO(
        name="John Doe",
        email=EmailAddress(address="some@example.com"),
        cpf=CPF(number="10856446696"),
    )

    creation_datetime = datetime.now()
    external_id = ExternalEntityId()

    customer_repository_mock.insert.return_value = Customer(
        name=customer_data.name,
        email=customer_data.email,
        created_at=creation_datetime,
        external_id=external_id,
        cpf=customer_data.cpf,
    )

    result = await create_customer_use_case_fx.execute(customer_data)

    assert result.name == "John Doe"
    assert result.email == EmailAddress(address="some@example.com")
    assert result.external_id == str(external_id)
    assert result.created_at == creation_datetime
    assert result.cpf == customer_data.cpf

    customer_repository_mock.insert.assert_called_once()


async def test_create_customer_that_already_exists() -> None:
    customer_repository_mock = Mock(spec=ICustomerRepository)
    create_customer_use_case_fx = CreateCustomerUseCase(customer_repository_mock)

    customer_data = CustomerCreationDTO(
        name="John Doe",
        email=EmailAddress(address="some@example.com"),
        cpf=CPF(number="10856446696"),
    )
    customer_repository_mock.insert.side_effect = DuplicateKeyError()

    with pytest.raises(DomainError) as exc_info:
        await create_customer_use_case_fx.execute(customer_data)

    assert exc_info.value.message == "Customer already exists"


async def test_create_customer_with_no_name_informed() -> None:
    customer_repository_mock = Mock(spec=ICustomerRepository)
    create_customer_use_case_fx = CreateCustomerUseCase(customer_repository_mock)

    customer_data = CustomerCreationDTO(
        name="",
        email=EmailAddress(address="some@example.com"),
        cpf=CPF(number="10856446696"),
    )

    with pytest.raises(ValidationError) as exc_info:
        await create_customer_use_case_fx.execute(customer_data)

    assert exc_info.value.message == "Validation error"
    errors = exc_info.value.errors
    assert len(errors) == 1

    err = next(iter(errors), None)
    assert err.msg == "String should have at least 3 characters"


async def test_create_customer_all_required_data_missing() -> None:
    customer_repository_mock = Mock(spec=ICustomerRepository)
    create_customer_use_case_fx = CreateCustomerUseCase(customer_repository_mock)

    # noinspection PyTypeChecker
    customer_data = CustomerCreationDTO(
        name=None,
        email=None,
        cpf=None,
    )

    with pytest.raises(ValidationError) as exc_info:
        await create_customer_use_case_fx.execute(customer_data)

    assert exc_info.value.message == "Validation error"
    errors = exc_info.value.errors
    assert len(errors) == 3

    err_messages = [err.msg for err in errors]

    assert "Input should be a valid string" in err_messages
    assert "Input should be an instance of CPF" in err_messages
    assert "Input should be an instance of EmailAddress" in err_messages

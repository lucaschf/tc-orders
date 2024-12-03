from datetime import datetime

import pytest

from src.domain.__shared.validator import ValidationError
from src.domain.__shared.value_objects import EmailAddress, CPF, ExternalEntityId
from src.domain.customer.entity import Customer
from tests.__providers import CPFProvider, UniqueEntityIdProvider


def test_customer_creation_successful() -> None:
    """Test successful customer creation."""
    name = "John Doe"
    cpf = CPF(number=CPFProvider.generate_cpf_number())
    email = EmailAddress(address="john.doe@example.com")

    customer = Customer(name=name, cpf=cpf, email=email)

    assert customer.name == name
    assert customer.cpf == cpf
    assert customer.email == email


def test_customer_creation_with_id_uuid_timestamps() -> None:
    """Test customer creation with optional parameters."""
    name = "Jane Smith"
    cpf = CPF(number=CPFProvider.generate_cpf_number())
    email = EmailAddress(address="jane.smith@example.com")
    _id = UniqueEntityIdProvider.generate_unique_entity_id()
    external_id = ExternalEntityId(id="12345678-1234-5678-1234-567812345678")

    created_at = datetime.now()

    customer = Customer(
        _id=_id,
        name=name,
        cpf=cpf,
        email=email,
        external_id=external_id,
        created_at=created_at,
    )

    assert customer._id == _id
    assert customer.external_id == external_id
    assert customer.created_at == created_at


def test_customer_creation_with_missing_name() -> None:
    cpf_str = CPFProvider.generate_cpf_number()

    with pytest.raises(ValidationError) as exec_info:
        Customer(
            name=None,  # type: ignore
            cpf=CPF(number=cpf_str),
            email=EmailAddress(address="john.doe@example.com"),
        )

    assert exec_info.value.message == "Validation error"
    assert len(exec_info.value.errors) == 1
    assert exec_info.value.errors[0].loc == ("name",)
    assert exec_info.value.errors[0].msg == "Input should be a valid string"


@pytest.mark.parametrize("name", ["", "    ", "a", "ab"])
def test_customer_creation_with_short_name(name: str | None) -> None:
    cpf_str = CPFProvider.generate_cpf_number()

    with pytest.raises(ValidationError) as exec_info:
        Customer(
            name=name,
            cpf=CPF(number=cpf_str),
            email=EmailAddress(address="john.doe@example.com"),
        )

    assert exec_info.value.message == "Validation error"
    assert len(exec_info.value.errors) == 1
    assert exec_info.value.errors[0].loc == ("name",)
    assert exec_info.value.errors[0].msg == "String should have at least 3 characters"


@pytest.mark.parametrize("name", ["a" * 256, "a" * 257])
def test_customer_creation_with_long_name(name: str) -> None:
    cpf_str = CPFProvider.generate_cpf_number()

    with pytest.raises(ValidationError) as exec_info:
        Customer(
            name=name,
            cpf=CPF(number=cpf_str),
            email=EmailAddress(address="john.doe@example.com"),
        )

    assert exec_info.value.message == "Validation error"
    assert len(exec_info.value.errors) == 1
    assert exec_info.value.errors[0].loc == ("name",)
    assert exec_info.value.errors[0].msg == "String should have at most 150 characters"


def test_customer_creation_with_missing_cpf() -> None:
    with pytest.raises(ValidationError) as exec_info:
        Customer(
            name="John Doe",
            cpf=None,  # type: ignore
            email=EmailAddress(address="john.doe@example.com"),
        )

    assert exec_info.value.message == "Validation error"
    assert len(exec_info.value.errors) == 1
    assert exec_info.value.errors[0].loc == ("cpf",)
    assert exec_info.value.errors[0].msg == "Input should be an instance of CPF"


def test_customer_creation_with_missing_email() -> None:
    with pytest.raises(ValidationError) as exec_info:
        Customer(
            name="John Doe",
            cpf=CPF(number=CPFProvider.generate_cpf_number()),
            email=None,  # type: ignore
        )

    assert exec_info.value.message == "Validation error"
    assert len(exec_info.value.errors) == 1
    assert exec_info.value.errors[0].loc == ("email",)
    assert (
        exec_info.value.errors[0].msg == "Input should be an instance of EmailAddress"
    )

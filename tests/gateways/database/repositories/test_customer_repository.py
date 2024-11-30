from datetime import datetime
from zoneinfo import ZoneInfo

import pytest
import time_machine

from __providers import CPFProvider
from src.domain.__shared.value_objects import (
    UniqueEntityId,
    CPF,
    EmailAddress,
)
from src.domain.customer import Customer
from src.infra.gateways.database.repositories.customer_repository_impl import (
    MongoCustomerRepository,
)


@time_machine.travel(
    datetime(2024, 2, 3, 5, 18, 29, 00, tzinfo=ZoneInfo("America/Sao_Paulo")),
    tick=False,
)
async def test_insert_returns_inserted_customer(initialize_database_fx):
    async with initialize_database_fx:
        customer = Customer(
            _id=UniqueEntityId("507f1f77bcf86cd799439011"),
            email=EmailAddress(address="test@example.com"),
            name="John Doe",
            cpf=CPF(number=CPFProvider.generate_cpf_number()),
        )

        repository = MongoCustomerRepository()
        result = await repository.insert(customer)
        assert result == customer


async def test_find_raises_value_error_when_no_criteria_provided():
    repository = MongoCustomerRepository()
    with pytest.raises(
        ValueError,
        match="At least one search criteria \\(CPF or email\\) must be provided",
    ):
        await repository.find(cpf=None, email=None)


@time_machine.travel(
    datetime(2024, 2, 3, 5, 18, 29, 00, tzinfo=ZoneInfo("America/Sao_Paulo")),
    tick=False,
)
async def test_find_returns_customer_when_cpf_is_provided(initialize_database_fx):
    async with initialize_database_fx:
        repository = MongoCustomerRepository()

        cpf = CPF(number=CPFProvider.generate_cpf_number())
        customer = Customer(
            _id=UniqueEntityId("507f1f77bcf86cd799439011"),
            email=EmailAddress(address="test@example.com"),
            name="John Doe",
            cpf=cpf,
        )

        await repository.insert(customer)

        result = await repository.find(cpf=cpf, email=None)
        assert result == customer


@time_machine.travel(
    datetime(2024, 2, 3, 5, 18, 29, 00, tzinfo=ZoneInfo("America/Sao_Paulo")),
    tick=False,
)
async def test_find_by_id_returns_customer_when_found(initialize_database_fx):
    async with initialize_database_fx:
        customer = Customer(
            _id=UniqueEntityId("507f1f77bcf86cd799439011"),
            email=EmailAddress(address="test@example.com"),
            name="John Doe",
            cpf=CPF(number=CPFProvider.generate_cpf_number()),
        )

        repository = MongoCustomerRepository()
        await repository.insert(customer)

        result = await repository.find_by_id("507f1f77bcf86cd799439011")
        assert result == customer


@time_machine.travel(
    datetime(2024, 2, 3, 5, 18, 29, 00, tzinfo=ZoneInfo("America/Sao_Paulo")),
    tick=False,
)
async def test_find_by_external_id_returns_customer_when_found(initialize_database_fx):
    async with initialize_database_fx:
        customer = Customer(
            _id=UniqueEntityId("507f1f77bcf86cd799439011"),
            email=EmailAddress(address="test@example.com"),
            name="John Doe",
            cpf=CPF(number=CPFProvider.generate_cpf_number()),
        )

        repository = MongoCustomerRepository()
        await repository.insert(customer)

        result = await repository.find_by_external_id(customer.external_id)
        assert result == customer

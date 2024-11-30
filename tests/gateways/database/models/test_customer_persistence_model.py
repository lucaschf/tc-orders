from datetime import datetime

from bson import ObjectId

from src.domain.__shared.value_objects import (
    ExternalEntityId,
    UniqueEntityId,
    EmailAddress,
    CPF,
)
from src.domain.customer import Customer
from src.infra.gateways.database.models.customer_persistence_model import (
    CustomerPersistenceModel,
)
from tests.__providers import CPFProvider


async def test_from_entity_creates_correct_persistence_model(initialize_database_fx):
    async with initialize_database_fx:
        cpf = CPF(number=CPFProvider.generate_cpf_number())
        external_id = ExternalEntityId()
        created_at = datetime.now()

        customer = Customer(
            _id=UniqueEntityId("507f1f77bcf86cd799439011"),
            external_id=external_id,
            created_at=created_at,
            email=EmailAddress(address="test@example.com"),
            name="John Doe",
            cpf=cpf,
        )

        persistence_model = CustomerPersistenceModel.from_entity(customer)

        assert persistence_model.id == ObjectId("507f1f77bcf86cd799439011")
        assert str(persistence_model.external_id) == str(external_id)
        assert persistence_model.created_at == created_at
        assert persistence_model.email == "test@example.com"
        assert persistence_model.name == "John Doe"
        assert persistence_model.cpf == cpf.number


async def test_to_entity_creates_correct_customer(initialize_database_fx):
    async with initialize_database_fx:
        cpf = CPF(number=CPFProvider.generate_cpf_number())
        external_id = ExternalEntityId()
        created_at = datetime.now()

        persistence_model = CustomerPersistenceModel(
            id=ObjectId("507f1f77bcf86cd799439011"),
            external_id=external_id.id,
            created_at=created_at,
            email="test@example.com",
            name="John Doe",
            cpf=cpf.number,
        )

        customer = persistence_model.to_entity()

        assert customer.id.id == "507f1f77bcf86cd799439011"
        assert customer.external_id.id == str(external_id)
        assert customer.created_at == created_at
        assert customer.email.address == "test@example.com"
        assert customer.name == "John Doe"
        assert persistence_model.cpf == cpf.number


async def test_from_entity_handles_none_id(initialize_database_fx):
    async with initialize_database_fx:
        cpf = CPF(number=CPFProvider.generate_cpf_number())
        external_id = ExternalEntityId()
        created_at = datetime.now()

        customer = Customer(
            _id=None,
            external_id=external_id,
            created_at=created_at,
            email=EmailAddress(address="test@example.com"),
            name="John Doe",
            cpf=cpf,
        )

        persistence_model = CustomerPersistenceModel.from_entity(customer)

        assert persistence_model.id is None
        assert str(persistence_model.external_id) == str(external_id)
        assert persistence_model.created_at == created_at
        assert persistence_model.email == "test@example.com"
        assert persistence_model.name == "John Doe"
        assert persistence_model.cpf == cpf.number

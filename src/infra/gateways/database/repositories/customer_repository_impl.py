from typing import Optional

from src.domain.__shared.error.repository_error import DuplicateKeyError
from src.domain.__shared.value_objects import (
    ExternalEntityId,
    UniqueEntityId,
    CPF,
    EmailAddress,
)
from src.domain.customer import Customer
from src.domain.customer.repository import ICustomerRepository
from src.infra.gateways.database.models import CustomerPersistenceModel
from pymongo.errors import DuplicateKeyError as MongoDuplicateKeyError


class MongoCustomerRepository(ICustomerRepository):
    """Repository for handling customer-related database operations."""

    async def find(
        self, cpf: CPF | None, email: EmailAddress | None
    ) -> Customer | None:
        if not cpf and not email:
            raise ValueError(
                "At least one search criteria (CPF or email) must be provided"
            )

        query = {}
        if cpf:
            query["cpf"] = cpf.number
        if email:
            query["email"] = email.address

        found = await CustomerPersistenceModel.find_one(query)
        return found.to_entity() if found else None

    async def insert(self, customer: Customer) -> Customer:
        try:
            persisted = await CustomerPersistenceModel.from_entity(customer).insert()
            return persisted.to_entity()
        except MongoDuplicateKeyError as e:
            raise DuplicateKeyError(str(e)) from e

    async def find_by_id(self, identifier: str | UniqueEntityId) -> Optional[Customer]:
        found = await CustomerPersistenceModel.get(str(identifier))
        return found.to_entity() if found else None

    async def find_by_external_id(
        self, external_id: str | ExternalEntityId
    ) -> Optional[Customer]:
        found = await CustomerPersistenceModel.find_one(
            {"external_id": str(external_id)}
        )
        return found.to_entity() if found else None


__all__ = ["MongoCustomerRepository"]

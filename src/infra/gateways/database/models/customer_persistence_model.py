from src.infra.gateways.database.models.base import PersistenceModel
from src.domain.__shared.value_objects import (
    ExternalEntityId,
    UniqueEntityId,
    EmailAddress,
    CPF,
)
from bson import ObjectId

from src.domain.customer import Customer


class CustomerPersistenceModel(PersistenceModel[Customer]):
    email: str
    name: str
    cpf: str

    @staticmethod
    def from_entity(entity: Customer) -> "CustomerPersistenceModel":
        return CustomerPersistenceModel(
            id=ObjectId(entity.id.id) if entity.id else None,
            external_id=str(entity.external_id),
            created_at=entity.created_at,
            email=entity.email.address,
            name=entity.name,
            cpf=entity.cpf.number,
        )

    def to_entity(self) -> Customer:
        return Customer(
            _id=UniqueEntityId(str(self.id)),
            external_id=ExternalEntityId(str(self.external_id)),
            created_at=self.created_at,
            email=EmailAddress(address=self.email),
            name=self.name,
            cpf=CPF(number=self.cpf),
        )


__all__ = ["CustomerPersistenceModel"]

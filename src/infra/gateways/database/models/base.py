from abc import abstractmethod, ABC
from datetime import datetime
from uuid import UUID

from beanie import Document
from domain.__shared.entity import AggregateRoot


class PersistenceModel[E: AggregateRoot](Document, ABC):
    external_id: UUID
    created_at: datetime

    @staticmethod
    @abstractmethod
    def from_entity(entity: E) -> "PersistenceModel[E]":
        pass

    @abstractmethod
    def to_entity(self) -> E:
        pass


__all__ = ["PersistenceModel"]

from abc import abstractmethod, ABC
from datetime import datetime
from typing import Annotated

from beanie import Document, Indexed

from src.domain.__shared.entity import AggregateRoot


class PersistenceModel[E: AggregateRoot](Document, ABC):
    external_id: Annotated[str, Indexed(unique=True)]
    created_at: datetime

    @staticmethod
    @abstractmethod
    def from_entity(entity: E) -> "PersistenceModel[E]":
        pass

    @abstractmethod
    def to_entity(self) -> E:
        pass


__all__ = ["PersistenceModel"]

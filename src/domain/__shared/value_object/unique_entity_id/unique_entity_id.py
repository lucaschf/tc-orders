from dataclasses import dataclass, field

from ...error import DomainError
from ..value_object import ValueObject
from .validator import UniqueEntityIdValidatorFactory


@dataclass(kw_only=True, frozen=True, slots=True)
class InvalidUniqueEntityIdError(DomainError):
    """Exception raised for invalid Unique Entity Ids."""

    message: str = "ID inválido"
    entity_id: str


@dataclass(frozen=True, slots=True)
class UniqueEntityId(ValueObject):
    """A Value Object that represents a unique entity identifier.

    It is used to uniquely identify entities in the domain model.
    """

    id: str = field()

    def __post_init__(self) -> None:
        self.__validate()

    def __validate(self) -> None:
        result = UniqueEntityIdValidatorFactory.create().validate(self.id)
        if not result.is_valid:
            raise InvalidUniqueEntityIdError(entity_id=self.id)


__all__ = ["InvalidUniqueEntityIdError", "UniqueEntityId"]

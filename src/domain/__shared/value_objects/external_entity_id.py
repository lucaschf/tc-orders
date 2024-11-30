from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID, uuid4

from ..error import DomainError
from .value_object import ValueObject


@dataclass(kw_only=True, frozen=True, slots=True)
class InvalidExternalIdError(DomainError):
    """Exception raised for invalid External Entity Ids."""

    external_entity_id: Optional[str]
    message: str = "ID inválido"


@dataclass(frozen=True, slots=True)
class ExternalEntityId(ValueObject):
    """Represents an external entity identifier.

    Attributes:
        id (str): The unique identifier for the external entity, defaulting to a new UUID.
    """

    id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        """Performs post-initialization validation and normalization of the `id` attribute."""
        object.__setattr__(
            self, "id", str(self.id) if isinstance(self.id, UUID) else self.id
        )
        self.__validate()

    def __validate(self) -> None:
        """Validates the UUID format of the id.

        Raises:
            InvalidExternalIdError: If the id is not a valid External ID.
        """
        try:
            UUID((str(self.id)))
        except (ValueError, TypeError) as ex:
            raise InvalidExternalIdError(external_entity_id=str(self.id)) from ex


__all__ = ["ExternalEntityId", "InvalidExternalIdError"]

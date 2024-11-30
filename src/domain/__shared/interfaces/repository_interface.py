from abc import ABC, abstractmethod
from typing import Optional

from src.domain.__shared.value_objects import ExternalEntityId, UniqueEntityId


class IRepository[T](ABC):
    """Interface for a generic repository.

    This interface defines the basic CRUD operations for a repository.
    """

    @abstractmethod
    def create(self, entity: T) -> T:
        """Create a new entity in the repository.

        Args:
            entity (T): The entity to be created.

        Returns:
            T: The created entity.

        Raises:
            DuplicatedKeyRepositoryError: If the entity already exists in the repository.
        """
        pass

    @abstractmethod
    def find_by_id(self, identifier: str | UniqueEntityId) -> Optional[T]:
        """Find an entity by its identifier.

        Args:
            identifier (str | UniqueEntityId): The identifier of the entity.

        Returns:
            Optional[T]: The found entity or None if not found.
        """
        pass

    @abstractmethod
    def find_by_external_id(self, external_id: str | ExternalEntityId) -> Optional[T]:
        """Find an entity by its external identifier.

        Args:
            external_id: The external identifier of the entity.

        Returns:
            Optional[T]: The found entity or None if not found.
        """
        pass


__all__ = ["IRepository"]

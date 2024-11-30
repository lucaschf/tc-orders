from src.domain.__shared.value_objects import UniqueEntityId
from bson import ObjectId


class UniqueEntityIdProvider:
    """Provider unique entity ids."""

    # noinspection PyMethodMayBeStatic
    def unique_entity_id(self) -> UniqueEntityId:
        """Return a random unique entity id."""
        return self.generate_unique_entity_id()

    @classmethod
    def generate_unique_entity_id(cls) -> UniqueEntityId:
        """Generate a unique entity id."""
        return UniqueEntityId(str(ObjectId()))


__all__ = ["UniqueEntityIdProvider"]

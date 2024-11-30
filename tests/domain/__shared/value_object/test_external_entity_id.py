from typing import Any

import pytest

from src.domain.__shared.value_objects import ExternalEntityId, InvalidExternalIdError


def test_external_entity_id_creation() -> None:
    """Test creating an ExternalEntityId with a default UUID."""
    entity_id = ExternalEntityId()
    assert isinstance(entity_id.id, str)
    assert entity_id.id


def test_external_entity_id_with_provided_uuid() -> None:
    """Test creating an ExternalEntityId with a specific UUID."""
    uuid_str = "123e4567-e89b-12d3-a456-426614174000"
    entity_id = ExternalEntityId(id=uuid_str)
    assert entity_id.id == uuid_str


@pytest.mark.parametrize("invalid_uuid", ["", " ", "not-a-uuid", None, 1234, {}, []])
def test_external_entity_id_invalid_uuid(invalid_uuid: Any) -> None:  # noqa: ANN401
    """Test that an InvalidUUIDError is raised for an invalid UUID."""
    with pytest.raises(InvalidExternalIdError):
        ExternalEntityId(id=invalid_uuid)


def test_external_entity_id_immutability() -> None:
    """Test that ExternalEntityId is immutable."""
    entity_id = ExternalEntityId()
    with pytest.raises(AttributeError):
        # noinspection PyDataclass
        entity_id.id = "new_uuid"

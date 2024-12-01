import uuid
from unittest.mock import Mock

import pytest
from pydantic import ValidationError
from pydantic_core import core_schema

from src.application.api.types.pydantic_external_id import PydanticExternalEntityId
from src.domain.__shared.value_objects import ExternalEntityId


def test_valid_external_entity_id() -> None:
    """Test that valid external ids are accepted."""
    valid_id_str = uuid.uuid4().hex
    valid_id = PydanticExternalEntityId(valid_id_str)
    assert valid_id == ExternalEntityId(id=valid_id_str).id


def test_invalid_external_entity_id_format() -> None:
    """Test that invalid external entity id formats raise ValueErrors."""
    invalid_id_str = "not_a_valid_id"
    with pytest.raises(ValueError) as exc_info:
        PydanticExternalEntityId(invalid_id_str)
    assert str(exc_info.value) == "Id inválido"


def test_invalid_external_entity_id_string_length() -> None:
    """Test that invalid external entity id string lengths raise errors."""
    invalid_id_str = "0"
    with pytest.raises(ValueError) as exc_info:
        PydanticExternalEntityId(invalid_id_str)
    assert str(exc_info.value) == "Id inválido"


def test_string_representation() -> None:
    """Test that the string representation is correct."""
    valid_id_str = "8a090307-b03d-4ecb-b5e3-2f4aeb623cf8"
    valid_id = PydanticExternalEntityId(valid_id_str)
    assert str(valid_id) == valid_id_str


def test_pydantic_validation() -> None:
    """Test validation within a Pydantic model."""
    from pydantic import BaseModel

    class MyModel(BaseModel):
        id: PydanticExternalEntityId

    # Valid ID
    valid_data = {"id": "8a090307-b03d-4ecb-b5e3-2f4aeb623cf8"}
    model = MyModel(**valid_data)
    assert model.id == PydanticExternalEntityId(valid_data["id"])

    # Invalid ID
    invalid_data = {"id": "not_a_valid_id"}
    with pytest.raises(ValidationError) as exc_info:
        MyModel(**invalid_data)
    assert exc_info.value.errors()[0]["msg"] == "Value error, Id inválido"


def test_domain_validation_error_handling() -> None:
    """Test if a domain validation exception handled correctly."""
    with pytest.raises(ValueError) as exc_info:
        PydanticExternalEntityId.validate("invalid_id", None)  # type: ignore
    assert str(exc_info.value) == "Id inválido"


def test_get_pydantic_json_schema() -> None:
    schema = Mock(spec=core_schema.CoreSchema)
    handler = Mock()

    handler.return_value = {}

    json_schema = PydanticExternalEntityId.__get_pydantic_json_schema__(schema, handler)

    expected_schema = {
        "type": "string",
        "example": "8a090307-b03d-4ecb-b5e3-2f4aeb623cf8",
    }

    assert json_schema == expected_schema

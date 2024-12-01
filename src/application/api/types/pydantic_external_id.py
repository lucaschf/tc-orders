from typing import Any, Type

from pydantic import GetCoreSchemaHandler, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from pydantic_core.core_schema import CoreSchema, ValidationInfo, str_schema

from src.domain.__shared.value_objects import ExternalEntityId, InvalidExternalIdError


class PydanticExternalEntityId(str):
    """A custom type for handling external entity IDs.

    This type ensures the ID is valid and provides a consistent representation.
    """

    # noinspection PyUnusedLocal
    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,  # noqa: ANN401
        handler: GetCoreSchemaHandler,
    ) -> CoreSchema:
        """Return a Pydantic core schema for this type."""
        return core_schema.json_or_python_schema(
            python_schema=core_schema.with_info_plain_validator_function(cls.validate),
            json_schema=str_schema(),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: str(instance)
            ),
        )

    @classmethod
    def validate(
        cls,
        v: Any,  # noqa: ANN401
        _: ValidationInfo | None = None,
    ) -> "PydanticExternalEntityId":
        """Validate the given external entity ID string.

        Args:
           v: The external entity ID to validate.
           _: Other values from the Pydantic model (unused for compatibility).

        Returns:
           The validated PydanticExternalEntityId.

        Raises:
           ValueError: If the PydanticExternalEntityId is invalid.
        """
        try:
            ExternalEntityId(id=v)
        except InvalidExternalIdError as error:
            raise ValueError("Id inválido") from error  # noqa: TRY003

        return v

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        schema: core_schema.CoreSchema,
        handler: GetJsonSchemaHandler,  # type: ignore
    ) -> JsonSchemaValue:
        json_schema = handler(schema)
        json_schema.update(
            type="string",
            example="8a090307-b03d-4ecb-b5e3-2f4aeb623cf8",
        )
        return json_schema

    def __new__(  # noqa: D102
        cls: Type["PydanticExternalEntityId"], value: str
    ) -> "PydanticExternalEntityId":
        return (  # type: ignore
            super(PydanticExternalEntityId, cls).__new__(cls, cls.validate(value))
        )


__all__ = ["PydanticExternalEntityId"]

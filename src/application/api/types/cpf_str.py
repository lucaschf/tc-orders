from typing import Any, Dict, Tuple, Type

from pydantic import GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema

from src.domain.__shared.value_objects import CPF, InvalidCPFError


class CPFStr(str):
    """A custom type for handling CPF strings.

    This type ensures that the CPF is valid and removes any mask, returning only the numeric
     characters.
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls: Type["CPFStr"],
        *_args: Tuple[()],
        **_kwargs: Dict[str, Any],
    ) -> core_schema.CoreSchema:
        """Return a Pydantic core schema for this type."""
        return core_schema.with_info_after_validator_function(
            cls._validate_and_remove_mask,
            core_schema.str_schema(),
        )

    @classmethod
    def _validate_and_remove_mask(
        cls: Type["CPFStr"],
        __input_value: str,
        _: core_schema.ValidationInfo | None = None,
    ) -> str:
        """Validate the given CPF string.

        Args:
            __input_value: The CPF string to validate.
            _: Other values from the Pydantic model. This argument is only for Pydantic
             compatibility and is not used.

        Returns:
            The validated and cleaned CPF string.

        Raises:
            ValueError if the CPF is invalid.
        """
        try:
            return CPF(number=__input_value).number
        except InvalidCPFError as error:
            raise ValueError(error.message) from error

    @classmethod
    def __get_pydantic_json_schema__(
        cls,
        schema: core_schema.CoreSchema,
        handler: GetJsonSchemaHandler,
    ) -> JsonSchemaValue:
        json_schema = handler(schema)
        json_schema.update(
            type="string",
            example="10856446696",
        )
        return json_schema

    def __new__(cls: Type["CPFStr"], cpf: str) -> "CPFStr":
        """Create a new instance of CPFStr.

        Args:
            cpf: The CPF string to validate and remove the mask from.

        Returns:
            A new CPFStr instance with the validated and cleaned CPF string.
        """
        return super(CPFStr, cls).__new__(cls, cls._validate_and_remove_mask(cpf))  # type: ignore


__all__ = ["CPFStr"]

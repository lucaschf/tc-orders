from abc import abstractmethod
from typing import Type

from pydantic import BaseModel, ValidationError
from pydantic_core import ErrorDetails

from .error_details import ValidationErrorDetails
from .error_translator import translate_pydantic_error_msg
from .validator_interface import IValidator, ValidationResult


class IPydanticValidator[T](IValidator):
    """An interface for Pydantic validators."""

    @abstractmethod
    def get_pydantic_model(self) -> Type[BaseModel]:
        """Gets the Pydantic model used for validation.

        Returns:
            BaseModel: The Pydantic model used for validation

        """

    @staticmethod
    def _translate_pydantic_error_msg(error: ErrorDetails) -> str:
        if custom_message := translate_pydantic_error_msg(error):
            ctx = error.get("ctx")
            return custom_message.format(**ctx) if ctx else custom_message

        if error.get("type") == "value_error":
            return error["msg"].replace("Value error, ", "")

        return error.get("msg")

    def validate(self, obj: T) -> ValidationResult:
        """Validates the provided object against the defined validation rules.

        Args:
            obj: The object to be validated.

        Returns:
            ValidationResult: The result of the validation operation.
        """
        try:
            self.get_pydantic_model().model_validate(obj, strict=True, from_attributes=True)
        except ValidationError as err:
            errors = [
                ValidationErrorDetails(
                    loc=error.get("loc"),
                    msg=self._translate_pydantic_error_msg(error)
                    if error.get("type") != "value_error"
                    else error.get("msg", "").replace("Value error, ", ""),
                )
                for error in err.errors()
            ]

            return ValidationResult(is_valid=False, errors=errors)

        return ValidationResult(is_valid=True)


__all__ = ["IPydanticValidator"]

from dataclasses import dataclass
from typing import Optional

from ...error import DomainError
from ..value_object import ValueObject
from .validator import EmailAddressValidatorFactory


@dataclass(frozen=True, kw_only=True, slots=True)
class InvalidEmailError(DomainError):
    """Exception raised when an email is invalid."""

    address: Optional[str]
    message: str = "Endereço de e-mail inválido."


@dataclass(frozen=True, kw_only=True, slots=True)
class EmailAddress(ValueObject):
    """A Value Object that represents an Email.

    This class validates the email using a simple regular expression.
    """

    address: str

    def __post_init__(self) -> None:
        """Validates the email address after initialization."""
        validation_result = EmailAddressValidatorFactory.create().validate(self)
        if not validation_result.is_valid:
            raise InvalidEmailError(address=self.address)


__all__ = ["EmailAddress", "InvalidEmailError"]

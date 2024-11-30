import re
from dataclasses import dataclass

from .value_object import ValueObject
from ..error import DomainError


@dataclass(frozen=True, kw_only=True, slots=True)
class InvalidCPFError(DomainError):
    """Exception raised when a CPF is invalid."""

    cpf: object | None = None
    message: str = "Invalid CPF."


@dataclass(frozen=True, kw_only=True, slots=True)
class CPF(ValueObject):
    """A Value Object that represents a Brazilian CPF (Cadastro de Pessoas Físicas).

    CPF is a unique number that identifies a taxpaying resident in Brazil. This class
    validates the CPF number using the official Brazilian algorithm.

    Attributes:
        number: The CPF number.
    """

    number: str

    def __post_init__(self) -> None:
        if not self._is_valid(self.number):
            raise InvalidCPFError(cpf=self.number)

        object.__setattr__(
            self,
            "number",
            self._clean_cpf(self.number)
            if isinstance(self.number, str)
            else self.number,
        )

    @classmethod
    def _is_valid(cls, cpf: str) -> bool:
        """Validates the input CPF number using the official Brazilian algorithm.

        Args:
            cpf (str): The CPF number to be validated.

        Returns:
            bool: True if the CPF number is valid, False otherwise.
        """
        if not re.match(r"(\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11})", cpf):
            return False

        cpf = cls._clean_cpf(cpf)

        # Checks if all digits are the same
        if cpf == cpf[0] * 11:
            return False

        checksum = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digit1 = 11 - (checksum % 11)
        digit1 = 0 if digit1 > 9 else digit1

        # Calculates the second check digit
        checksum = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digit2 = 11 - (checksum % 11)
        digit2 = 0 if digit2 > 9 else digit2

        return cpf.endswith(f"{digit1}{digit2}")

    @staticmethod
    def _clean_cpf(cpf: str) -> str:
        """Removes non-digit characters from the CPF number.

        Args:
            cpf (str): The CPF number to be cleaned.

        Returns:
            str: The cleaned CPF number.
        """
        return re.sub(r"\D", "", cpf)


__all__ = ["CPF", "InvalidCPFError"]

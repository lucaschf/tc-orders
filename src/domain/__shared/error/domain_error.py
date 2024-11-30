from dataclasses import dataclass
from typing import Optional


@dataclass(kw_only=True, frozen=True, slots=True)
class DomainError(Exception):
    """A custom exception class used to handle domain-specific exceptions."""

    message: Optional[str] = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message={self.message!r})"

    def __str__(self) -> str:
        return repr(self)


__all__ = ["DomainError"]

from dataclasses import dataclass

from src.application.error import NotFoundError


@dataclass(frozen=True, kw_only=True, slots=True)
class CustomerNotFoundError(NotFoundError):
    """Error for when a customer is not found."""

    search_params: dict[str, str]


__all__ = ["CustomerNotFoundError"]

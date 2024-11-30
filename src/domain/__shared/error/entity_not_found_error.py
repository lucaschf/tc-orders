from dataclasses import dataclass
from typing import Dict, Optional

from .domain_error import DomainError


@dataclass(frozen=True, kw_only=True, slots=True)
class EntityNotFoundError(DomainError):
    """Base class for errors where an entity is not found."""

    search_params: Dict[str, Optional[object]]


__all__ = ["EntityNotFoundError"]

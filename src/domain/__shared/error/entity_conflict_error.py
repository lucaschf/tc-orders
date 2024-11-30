from dataclasses import dataclass
from typing import Dict

from .domain_error import DomainError


@dataclass(frozen=True, kw_only=True, slots=True)
class EntityConflictError(DomainError):
    """Exception raised for conflicts in the domain."""

    message: str = "Dados conflitantes"
    conflict_params: Dict[str, object]


__all__ = ["EntityConflictError"]

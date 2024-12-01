from dataclasses import dataclass
from typing import Dict, Optional

from src.domain.__shared.error import DomainError


@dataclass(kw_only=True, frozen=True, slots=True)
class RepositoryError(DomainError):
    """Base class for all repository errors."""

    message: str = "Erro no repositório"


@dataclass(frozen=True, kw_only=True, slots=True)
class DuplicateKeyError(RepositoryError):
    """Raised when a record with a duplicated key is attempted to be inserted."""

    message: str = "Chave duplicada encontrada"


@dataclass(frozen=True, kw_only=True, slots=True)
class RecordNotFoundError(RepositoryError):
    """Raised when an entity is not found in the repository."""

    message: str = "Registro não encontrado"
    entity_class: Optional[type] = None
    search_params: Optional[Dict[str, object]] = None

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(message={self.message!r}, "
            f"entity_class={self.entity_class!r}, "
            f"search_params={self.search_params!r})"
        )


__all__ = [
    "DuplicateKeyError",
    "RecordNotFoundError",
    "RepositoryError",
]

from typing import Any

from pydantic import BaseModel


class HttpErrorOut(BaseModel):
    """Basic error response model."""

    detail: Any = None


__all__ = ["HttpErrorOut"]

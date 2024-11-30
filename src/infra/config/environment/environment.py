from enum import StrEnum, auto


class Environment(StrEnum):
    """The different application environments."""

    DEV = auto()
    PROD = auto()
    TEST = auto()


__all__ = [
    "Environment",
]

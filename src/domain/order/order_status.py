from enum import StrEnum, auto
from typing import Iterable, Dict


class OrderStatus(StrEnum):
    """An Enum that represents an Order Status."""

    PAYMENT_PENDING = auto()
    RECEIVED = auto()
    PROCESSING = auto()
    READY = auto()
    COMPLETED = auto()

    @classmethod
    def values(cls) -> Iterable["OrderStatus"]:
        """Return a list of OrderStatus values."""
        return [cls(member) for member in cls.__members__]

    def get_allowed_transitions(self) -> Iterable["OrderStatus"]:
        """Returns the allowed transitions for the given status."""
        _transitions: Dict["OrderStatus", Iterable["OrderStatus"]] = {
            OrderStatus.PAYMENT_PENDING: [OrderStatus.RECEIVED],
            OrderStatus.RECEIVED: [OrderStatus.PROCESSING],
            OrderStatus.PROCESSING: [OrderStatus.READY],
            OrderStatus.READY: [OrderStatus.COMPLETED],
        }

        return _transitions.get(self, [])


__all__ = ["OrderStatus"]

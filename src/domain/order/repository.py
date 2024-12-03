from abc import ABC, abstractmethod
from typing import List

from src.domain.__shared.interfaces import IRepository
from src.domain.order import Order


class IOrderRepository(IRepository[Order], ABC):
    @abstractmethod
    async def list_all(self) -> List[Order]:
        """Retrieves all orders from the repository.

        Returns:
            List[Order]: A list of all orders.
        """
        pass


__all__ = ["IOrderRepository"]

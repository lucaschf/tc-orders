from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Product:
    id: str
    name: str
    price: float


class IProductService(ABC):
    @abstractmethod
    def fetch_products_by_ids(self, ids: List[str]) -> List[Product]:
        pass


__all__ = ["IProductService", "Product"]

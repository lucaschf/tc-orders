from typing import List

import requests

from src.domain.__shared.error.external_service_error import ExternalServiceError
from src.domain.__shared.interfaces.product_service import IProductService, Product


class ProductServiceImpl(IProductService):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def fetch_products_by_ids(self, ids: List[str]) -> List[Product]:
        products = []
        for product_id in ids:
            try:
                response = requests.get(f"{self.base_url}/products/{product_id}")
                response.raise_for_status()
                products.append(
                    Product(
                        id=response.json()["id"],
                        name=response.json()["name"],
                        price=response.json()["price"],
                    )
                )
            except requests.HTTPError as http_err:
                raise ExternalServiceError(
                    message=f"Failed to fetch product {product_id}: {http_err}",
                    status_code=http_err.response.status_code,
                ) from http_err
            except requests.RequestException as err:
                raise ExternalServiceError(
                    message=f"An error occurred while fetching product {product_id}: {err}",
                    status_code=500,
                ) from err
        return products


__all__ = ["ProductServiceImpl"]

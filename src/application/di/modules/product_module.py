from injector import Module, provider, singleton

from src.domain.__shared.interfaces import IProductService
from src.infra.gateways.external_services.product_service import ProductServiceImpl


class ProductModule(Module):
    """Dependency injection module for the Order domain."""

    @singleton
    @provider
    def provide_product_service(self) -> IProductService:
        """Provide the order repository."""
        return ProductServiceImpl()


__all__ = ["ProductModule"]

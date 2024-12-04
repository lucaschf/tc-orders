from injector import Binder, Injector

from src.application.di.modules import CustomerModule
from src.application.di.modules.order_module import OrderModule
from src.application.di.modules.product_module import ProductModule


def configure_injector(binder: Binder) -> None:  # noqa: ARG001
    """Configures the injector by installing the Modules."""
    binder.install(CustomerModule())
    binder.install(ProductModule())
    binder.install(OrderModule())


dependency_injector = Injector([configure_injector])

__all__ = ["dependency_injector"]

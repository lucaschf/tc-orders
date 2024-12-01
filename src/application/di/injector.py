from injector import Binder, Injector

from src.application.di.modules import CustomerModule


def configure_injector(binder: Binder) -> None:  # noqa: ARG001
    """Configures the injector by installing the Modules."""
    binder.install(CustomerModule())


dependency_injector = Injector([configure_injector])

__all__ = ["dependency_injector"]

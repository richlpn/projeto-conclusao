from typing import Optional, Type

from dependency_injector.providers import Singleton
from src.config.dependency_injection.container import Container


def component(interface: Optional[Type] = None):
    """
    Decorator to register a class as a component in the container
    Args:
        interface: Optional interface this class implements.
                 If None, the class itself is used as the key
    """

    def decorator(cls):
        key_type = interface if interface is not None else cls
        Container._instances[key_type] = Singleton(cls)
        return cls

    return decorator

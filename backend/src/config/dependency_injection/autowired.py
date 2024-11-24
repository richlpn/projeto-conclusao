from functools import wraps
from typing import Callable, TypeVar, get_type_hints

from src.config.dependency_injection.container import Container

T = TypeVar("T")


def autowired(func: Callable) -> Callable:
    """
    Decorator that automatically injects dependencies based on type hints
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        params = []
        for param, cls in get_type_hints(func).items():
            if param == "return":
                continue
            instance = Container.get_instance(cls)
            params.append(instance)
        return func(args[0], *params, **kwargs)

    return wrapper

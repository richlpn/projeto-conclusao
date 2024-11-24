from typing import Any, Type, TypeVar
from dependency_injector import containers
from src.exceptions.depencency_exceptions import DependencyNotFoundError

T = TypeVar("T")


class Container(containers.DeclarativeContainer):

    _instances: dict[Type, Any] = {}

    @classmethod
    def get_instance(cls, type_):
        """Get or create an instance of the requested type"""
        if type_ not in cls._instances:
            raise DependencyNotFoundError(type_)
        return cls._instances[type_]()

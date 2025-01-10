from abc import ABC, abstractmethod
from typing import Generic, TypeVar

OutputType = TypeVar("OutputType")


class CrudService(ABC, Generic[OutputType]):

    @abstractmethod
    def __init__(): ...

    @abstractmethod
    def create(self, *args, **kwargs) -> OutputType: ...

    @abstractmethod
    def get_by_id(self, *args, **kwargs) -> OutputType: ...

    @abstractmethod
    def update(self, *arg, **kwargs) -> OutputType: ...
    @abstractmethod
    def delete(self, *args, **kwargs): ...
    @abstractmethod
    def get_all(self, *args, **kwargs) -> list[OutputType]: ...

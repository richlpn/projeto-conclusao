from typing import Generic, TypeVar, Optional, List
from abc import ABC, abstractmethod
from pydantic import BaseModel
from src.utils.base_repository import BaseRepository
from src.utils.base_schema import BaseSchema

ModelType = TypeVar("ModelType", bound=BaseModel)
InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")
IDType = TypeVar("IDType")


class BaseService(ABC, Generic[ModelType, InputType, IDType]):

    def __init__(self, repository: BaseRepository[ModelType, IDType]):
        self.repository = repository

    @abstractmethod
    def create(self, dto: InputType) -> BaseSchema[ModelType]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: IDType) -> Optional[BaseSchema[ModelType]]:
        raise NotImplementedError

    @abstractmethod
    def update(self, id: IDType, dto: InputType) -> Optional[BaseSchema[ModelType]]:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: IDType) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_all(self, skip: int = 0, limit: int = 100) -> List[BaseSchema[ModelType]]:
        raise NotImplementedError

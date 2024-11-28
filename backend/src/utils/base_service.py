from abc import ABC
from typing import Generic, List, Optional, Type, TypeVar

from fastapi import HTTPException
from src.config.database import Base
from src.utils.base_repository import BaseRepository
from src.utils.base_schema import BaseSchema

ModelType = TypeVar("ModelType", bound=Base)  # type: ignore
InputType = TypeVar("InputType", bound=BaseSchema)
UpdateType = TypeVar("UpdateType", bound=BaseSchema)
IDType = TypeVar("IDType")


class BaseService(ABC, Generic[ModelType, InputType, UpdateType, IDType]):

    def __init__(
        self,
        model: Type[ModelType],
        repository: BaseRepository[ModelType, IDType],
    ):
        self.model = model
        self.repository = repository

    def create(self, obj: InputType) -> ModelType:
        db_obj: ModelType = self.model(**obj.model_dump())
        self.repository.create(db_obj)
        return db_obj

    def get_by_id(self, id: IDType) -> Optional[ModelType]:
        obj: Optional[ModelType] = self.repository.get_by_id(id)
        if obj is None:
            raise HTTPException(status_code=404, detail="Not Found")
        return obj

    def update(self, id: IDType, obj: UpdateType) -> Optional[ModelType]:
        db_obj = self.repository.get_by_id(id)
        if db_obj is None:
            raise HTTPException(status_code=404, detail="Not Found")

        for column, value in obj.model_dump(exclude_unset=True).items():
            setattr(db_obj, column, value)
        self.repository.update(db_obj)
        return db_obj

    def delete(self, id: IDType):
        db_obj = self.repository.delete(id)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        objs: List[ModelType] = self.repository.get_all(skip, limit)
        return objs

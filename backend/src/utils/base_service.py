from abc import ABC
from typing import Generic, List, Optional, Type, TypeVar

from fastapi import HTTPException
from src.config.database import Base
from src.utils.base_repository import BaseRepository
from src.utils.base_schema import BaseSchema

ModelType = TypeVar("ModelType", bound=Base)  # type: ignore
InputType = TypeVar("InputType", bound=BaseSchema)
UpdateType = TypeVar("UpdateType", bound=BaseSchema)
OutputType = TypeVar("OutputType", bound=BaseSchema)
IDType = TypeVar("IDType")


class BaseService(ABC, Generic[ModelType, InputType, UpdateType, OutputType, IDType]):

    def __init__(
        self,
        model: Type[ModelType],
        schema: Type[OutputType],
        repository: BaseRepository[ModelType, IDType],
    ):
        self.model = model
        self.schema = schema
        self.repository = repository

    def create(self, obj: InputType) -> OutputType:
        schema = self.schema(**obj.model_dump())
        db_obj: ModelType = self.model(**schema.model_dump())
        self.repository.create(db_obj)
        return schema

    def get_by_id(self, id: IDType) -> OutputType:
        obj: Optional[ModelType] = self.repository.get_by_id(id)
        if obj is None:
            raise HTTPException(status_code=404, detail="Not Found")
        return self.schema(**obj.__dict__)

    def update(self, id: IDType, obj: UpdateType) -> OutputType:
        db_obj = self.repository.get_by_id(id)
        if db_obj is None:
            raise HTTPException(status_code=404, detail="Not Found")

        for column, value in obj.model_dump(exclude_unset=True).items():
            setattr(db_obj, column, value)
        schema = self.schema(**db_obj.__dict__)
        self.repository.update(db_obj)
        return schema

    def delete(self, id: IDType):
        db_obj = self.repository.delete(id)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[OutputType]:
        objs: List[ModelType] = self.repository.get_all(skip, limit)
        return [self.schema(**obj.__dict__) for obj in objs]

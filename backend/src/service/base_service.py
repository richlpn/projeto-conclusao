from typing import Generic, List, Optional, Type, TypeVar

from fastapi import HTTPException
from src.config.database import Base
from src.repositories.base_repository import BaseRepository
from src.schema.base_schema import BaseSchema
from src.service.crud_service import CrudService

ModelType = TypeVar("ModelType", bound=Base)  # type: ignore
InputType = TypeVar("InputType", bound=BaseSchema)
UpdateType = TypeVar("UpdateType", bound=BaseSchema)
OutputType = TypeVar("OutputType", bound=BaseSchema)
IDType = TypeVar("IDType")


class BaseService(
    CrudService[OutputType],
    Generic[ModelType, InputType, UpdateType, OutputType, IDType],
):

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
        schema = self.schema.model_validate(obj.model_dump())
        db_obj: ModelType = self.model(**schema.model_dump())
        self.repository.create(db_obj)
        return schema

    def get_by_id(self, id: IDType) -> OutputType:
        obj: Optional[ModelType] = self.repository.get_by_id(id)
        if obj is None:
            raise HTTPException(status_code=404, detail="Not Found")
        return self.schema.model_validate(obj)

    def update(self, id: IDType, obj: UpdateType) -> OutputType:
        db_obj = self.repository.get_by_id(id)
        if db_obj is None:
            raise HTTPException(status_code=404, detail="Not Found")

        orinal_schema = self.schema.model_validate(db_obj)
        schema = orinal_schema.model_copy(update=obj.model_dump(exclude_unset=True))
        db_obj = self.model(**schema.model_dump())

        self.repository.update(db_obj)
        return schema

    def delete(self, id: IDType):
        return self.repository.delete(id)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[OutputType]:
        objs: List[ModelType] = self.repository.get_all(skip, limit)
        return [self.schema.model_validate(obj) for obj in objs]

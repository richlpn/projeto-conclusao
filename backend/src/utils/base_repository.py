from abc import ABC
from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy.exc import NoInspectionAvailable
from sqlalchemy.inspection import inspect
from src.config.database import create_session

T = TypeVar("T")
IDType = TypeVar("IDType")


class BaseRepository(ABC, Generic[T, IDType]):

    model: Type[T]

    def __init__(self):
        self.db = create_session()
        self.primary_key = self._get_primary_key()

    def create(self, obj_in: T) -> T:
        self.db.add(obj_in)
        self.db.commit()
        return obj_in

    def get_by_id(self, id: IDType) -> Optional[T]:
        id_col = self.primary_key
        return self.db.query(self.model).filter(id_col == id).first()

    def update(self, new_obj: T) -> Optional[T]:
        self.db.add(new_obj)
        return new_obj

    def delete(self, id: IDType) -> bool:
        db_obj = self.get_by_id(id)
        if db_obj:
            self.db.delete(db_obj)
            return True
        return False

    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def _get_primary_key(self):
        inspection = inspect(self.model)
        if not inspection:
            raise NoInspectionAvailable(
                f"Unable to determine primary key for model {self.model.__name__}"
            )
        return inspection.primary_key[0]

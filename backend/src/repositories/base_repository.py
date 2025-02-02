from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy.exc import NoInspectionAvailable
from sqlalchemy.inspection import inspect
from src.config.database.database import scoped_session
from src.config.database.handle_query_exception import handle_sqlalchemy_session

T = TypeVar("T")
IDType = TypeVar("IDType")


class BaseRepository(Generic[T, IDType]):

    model: Type[T]
    db: scoped_session

    def __init__(self, model: Type[T]):
        self.model = model
        self.primary_key = self._get_primary_key()

    @handle_sqlalchemy_session
    def create(self, obj_in: T) -> T:
        self.db.add(obj_in)
        return obj_in

    @handle_sqlalchemy_session
    def get_by_id(self, id: IDType) -> Optional[T]:
        id_col = self.primary_key
        return self.db.query(self.model).filter(id_col == id).first()

    @handle_sqlalchemy_session
    def update(self, new_obj: T) -> Optional[T]:
        self.db.commit()
        return new_obj

    @handle_sqlalchemy_session
    def delete(self, id: IDType) -> bool:
        db_obj = self.get_by_id(id)
        if db_obj:
            self.db.delete(db_obj)
            return True
        return False

    @handle_sqlalchemy_session
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def _get_primary_key(self, obj=None):
        if not obj:
            obj = self.model
        inspection = inspect(obj)
        if not inspection:
            raise NoInspectionAvailable(
                f"Unable to determine primary key for model {obj.__name__}"
            )
        return inspection.primary_key[0]

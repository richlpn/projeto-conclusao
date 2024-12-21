from functools import wraps
from inspect import signature
from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy import and_, or_
from sqlalchemy.exc import NoInspectionAvailable
from sqlalchemy.inspection import inspect
from src.config.database import create_session

T = TypeVar("T")
IDType = TypeVar("IDType")


def query(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # Parse the function name
        func_name = func.__name__
        if not func_name.startswith("filter_by_"):
            raise ValueError(
                f"Function name '{func_name}' must start with 'filter_by_'."
            )

        # Extract attributes and logical operator from the function name
        query_parts = (
            func_name[10:].split("_and_")
            if "_and_" in func_name
            else func_name[10:].split("_or_")
        )
        operator = and_ if "_and_" in func_name else or_

        # Map arguments to their corresponding model attributes
        sig = signature(func)
        bound_args = sig.bind(self, *args, **kwargs)
        bound_args.apply_defaults()  # Apply default values if any

        filters = [
            getattr(self.model, attr) == bound_args.arguments[attr]
            for attr in query_parts
            if attr in bound_args.arguments
        ]

        # Execute the query using SQLAlchemy
        return self.db.query(self.model).filter(operator(*filters)).all()

    return wrapper


class BaseRepository(Generic[T, IDType]):

    model: Type[T]

    def __init__(self, model: Type[T]):
        self.model = model
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
            self.db.commit()
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

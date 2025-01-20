from functools import wraps
from inspect import signature
from typing import Callable, Generic, List, Optional, Type, TypeVar

from sqlalchemy import and_, or_
from sqlalchemy.exc import NoInspectionAvailable, SQLAlchemyError
from sqlalchemy.inspection import inspect
from src.config.database import create_session

T = TypeVar("T")
IDType = TypeVar("IDType")


def handle_sqlalchemy_exceptions(func):
    """
    A decorator to handle SQLAlchemy exceptions for class methods.
    Rolls back the transaction in case of an error.
    """

    @wraps(func)
    def wrapper(self: "BaseRepository", *args, **kwargs):
        try:
            # Execute the decorated function
            result = func(self, *args, **kwargs)
            # Commit the transaction if successful
            self.db.commit()
            return result
        except SQLAlchemyError as e:
            # Rollback the transaction on error
            self.db.rollback()
            raise e  # Re-raise the exception for external handling

    return wrapper


def query(func: Callable) -> Callable:
    """
    Decorator that generates SQLAlchemy queries based on function names.
    Supports operations: eq, gt, lt, not_eq
    Format: filter_by_[field]_[operation]_[field]_[operation]_[logic]
    Example: filter_by_age_gt_and_salary_lt
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        func_name = func.__name__
        if not func_name.startswith("filter_by_"):
            raise ValueError(
                f"Function name '{func_name}' must start with 'filter_by_'"
            )

        # Determine logical operator
        is_and = "_and_" in func_name
        operator = and_ if is_and else or_

        # Split into operation parts
        parts = func_name[10:].split("_and_" if is_and else "_or_")

        # Bind arguments
        sig = signature(func)
        bound_args = sig.bind(self, *args, **kwargs)
        bound_args.apply_defaults()

        filters = []
        for part in parts:
            # Parse operation type (gt, lt, eq, not_eq)
            segments = part.split("_")
            if len(segments) == 1:  # Default to eq
                field, op = segments[0], "eq"
            else:
                field, op = segments[0], segments[1]

            if field not in bound_args.arguments:
                continue

            value = bound_args.arguments[field]
            model_attr = getattr(self.model, field)

            # Apply operation
            if op == "gt":
                filters.append(model_attr > value)
            elif op == "lt":
                filters.append(model_attr < value)
            elif op == "not_eq":
                filters.append(model_attr != value)
            else:  # eq is default
                filters.append(model_attr == value)

        return self.db.query(self.model).filter(operator(*filters)).all()

    return wrapper


class BaseRepository(Generic[T, IDType]):

    model: Type[T]

    def __init__(self, model: Type[T]):
        self.model = model
        self.db = create_session()
        self.primary_key = self._get_primary_key()

    @handle_sqlalchemy_exceptions
    def create(self, obj_in: T) -> T:
        self.db.add(obj_in)
        return obj_in

    @handle_sqlalchemy_exceptions
    def get_by_id(self, id: IDType) -> Optional[T]:
        id_col = self.primary_key
        return self.db.query(self.model).filter(id_col == id).first()

    @handle_sqlalchemy_exceptions
    def update(self, new_obj: T) -> Optional[T]:
        merged = self.db.merge(new_obj)
        self.db.flush()
        return new_obj

    @handle_sqlalchemy_exceptions
    def delete(self, id: IDType) -> bool:
        db_obj = self.get_by_id(id)
        if db_obj:
            self.db.delete(db_obj)
            return True
        return False

    @handle_sqlalchemy_exceptions
    def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def _get_primary_key(self):
        inspection = inspect(self.model)
        if not inspection:
            raise NoInspectionAvailable(
                f"Unable to determine primary key for model {self.model.__name__}"
            )
        return inspection.primary_key[0]

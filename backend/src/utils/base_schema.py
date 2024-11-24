from abc import ABC, abstractmethod
from typing import Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class BaseSchema(ABC, BaseModel, Generic[T]):
    """
    Abstract base class for creating Pydantic schemas from models.

    This class provides a basic structure for creating schemas that can be used to
    validate and serialize data. It uses Pydantic's BaseModel for validation and
    serialization, and adds an abstract method for creating the schema from a model.

    Type parameter T represents the type of the model that the schema is created from.
    """

    @abstractmethod
    def to_model(self) -> T:
        """
        Creates a schema instance from a model.

        Args:
            model: The model instance to create the schema from.

        Returns:
            A schema instance representing the model.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        ...

    @classmethod
    @abstractmethod
    def from_model(cls, model: T) -> "BaseSchema[T]":
        raise NotImplementedError()

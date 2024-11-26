from abc import ABC
from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


def to_camel(string: str) -> str:
    if "_" not in string:
        return string
    words = string.split("_")
    words = [words[0]] + [word.capitalize() for word in words[1:]]
    return "".join(words)


class BaseSchema(ABC, BaseModel, Generic[T]):
    """
    Abstract base class for creating Pydantic schemas from models.

    This class provides a basic structure for creating schemas that can be used to
    validate and serialize data. It uses Pydantic's BaseModel for validation and
    serialization, and adds an abstract method for creating the schema from a model.

    Type parameter T represents the type of the model that the schema is created from.
    """

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True

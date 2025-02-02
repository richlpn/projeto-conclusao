from typing import TypeVar

from pydantic import BaseModel
from src.utils import to_camel

T = TypeVar("T")


class BaseSchema(BaseModel):
    """
    Abstract base class for creating Pydantic schemas from models.

    This class provides a basic structure for creating schemas that can be used to
    validate and serialize data. It uses Pydantic's BaseModel for validation and
    serialization, and adds an abstract method for creating the schema from a model.

    Type parameter T represents the type of the model that the schema is created from.
    """

    class Config:
        alias_generator = to_camel
        populate_by_name = True

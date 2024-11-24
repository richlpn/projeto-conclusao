from abc import ABC, abstractmethod
from typing import ClassVar, Generic, Type, TypeVar
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase

M = TypeVar("M", bound=DeclarativeBase)  # type: ignore
S = TypeVar("S", bound=BaseModel)  # type: ignore


class DTOMetaclass(type(BaseModel)):
    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super().__new__(mcs, name, bases, namespace, **kwargs)
        if bases and bases[0] != BaseModel:
            model_type = getattr(cls, "__orig_bases__", [None])[0]
            if model_type and hasattr(model_type, "__args__"):
                cls.__model__ = model_type.__args__[0]
        return cls


class BaseDTO(ABC, BaseModel, Generic[M], metaclass=DTOMetaclass):

    __model__: ClassVar[Type[M]]  # type: ignore

    class Config:
        from_attributes = True

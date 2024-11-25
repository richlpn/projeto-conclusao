from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from src.utils.base_dto import BaseDTO
from src.utils.base_service import BaseService

ServiceType = TypeVar("ServiceType", bound=BaseService)
InputType = TypeVar("InputType", bound=BaseDTO)
OutputType = TypeVar("OutputType")
IDType = TypeVar("IDType")


class BaseController(ABC, Generic[ServiceType, InputType, OutputType, IDType]):
    """
    An abstract base class for controllers that provides a standard interface for CRUD operations.

    This class defines the basic methods for creating, reading, updating, and deleting data, and is intended to be subclassed by concrete controller classes.

    Type Parameters:
        ServiceType: The type of the service that the controller will use to interact with the data.
        InputType: The type of the input data that the controller will accept.
        OutputType: The type of the output data that the controller will return.
        IDType: The type of the ID that will be used to identify individual data items.

    Attributes:
        service: An instance of the service that the controller will use to interact with the data.

    Methods:
        get(id: IDType) -> OutputType: Retrieves a single data item by its ID.
        get_all() -> Iterable[OutputType]: Retrieves all data items.
        create(input: InputType) -> OutputType: Creates a new data item.
        update(id: IDType, input: InputType) -> OutputType: Updates an existing data item.
        delete(id: IDType): Deletes a data item by its ID.

    Note:
        This class is abstract and cannot be instantiated directly. Concrete subclasses must implement all of the abstract methods.
    """

    def __init__(self, service: ServiceType, *args, **kwargs) -> None:
        self.service = service

    @abstractmethod
    async def get(self, id: IDType, *args, **kwargs) -> OutputType:
        raise NotImplementedError()

    @abstractmethod
    async def get_all(self, skip: int, limit: int, *args, **kwargs) -> list[OutputType]:
        raise NotImplementedError()

    @abstractmethod
    async def create(self, input: InputType, *args, **kwargs) -> OutputType:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, id: IDType, input: InputType, *args, **kwargs) -> OutputType:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, id: IDType, *args, **kwargs):
        raise NotImplementedError()

from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import ValidationError
from src.config.controller import controller
from src.config.dependency_injection.autowired import autowired
from src.schema.data_source_schema import BaseSchema, DataSource, DataSourceSchema
from src.service.data_source_service import (
    BaseService,
    DataSourceService,
    DataSourceDTO,
)
from src.utils.base_controller import BaseController
from src.utils.base_dto import BaseDTO

router = APIRouter(prefix="/data-sources", tags=["Data Sources"])


@controller(router)
class DataSourceController(
    BaseController[
        BaseService[DataSource, DataSourceDTO, UUID],
        BaseDTO[DataSource],
        BaseSchema[DataSource],
        UUID,
    ]
):

    @autowired
    def __init__(self, service: DataSourceService) -> None:
        super().__init__(service)

    @router.get("/", response_model=DataSourceSchema, status_code=status.HTTP_200_OK)
    async def get(self, id: UUID) -> BaseSchema[DataSource]:
        obj = self.service.get_by_id(id)
        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Object with ID `{id}` was not found.",
            )
        return obj

    @router.get("/all", response_model=None)
    async def get_all(self, *args, **kwargs) -> list[BaseSchema[DataSource]]:
        return self.service.get_all(skip, limit)  # type: ignore

    @router.post(
        "/", response_model=DataSourceSchema, status_code=status.HTTP_201_CREATED
    )
    async def create(self, input: DataSourceDTO) -> BaseSchema[DataSource]:
        try:
            return self.service.create(input)
        except ValidationError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    @router.delete("/", status_code=status.HTTP_200_OK)
    async def delete(self, id: UUID):
        """
        Delete a data source.

        Args:
        - name: The name of the data source.
        """
        obj = self.service.delete(id)

        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Object with ID `{id}` was not found.",
            )

    @router.patch("/", status_code=status.HTTP_200_OK)
    async def update(self, id: UUID, input: DataSourceDTO) -> BaseSchema[DataSource]:
        obj = self.service.update(id, input)

        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Object with ID `{id}` was not found.",
            )
        return obj

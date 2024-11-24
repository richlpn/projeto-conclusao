from typing import Iterable
from uuid import UUID

from fastapi import APIRouter, HTTPException, status
from pydantic import ValidationError
from src.config.controller import controller
from src.config.dependency_injection.autowired import autowired
from src.models.dtos.data_source_dto import DataSourceDTO
from src.schema.data_source_schema import DataSourceSchema
from src.service.data_source_service import DataSourceService
from src.utils.base_controller import BaseController

router = APIRouter(prefix="/data-sources", tags=["Data Sources"])


@controller(router)
class DataSourceController(
    BaseController[DataSourceService, DataSourceDTO, DataSourceSchema, UUID]
):

    @autowired
    def __init__(self, service: DataSourceService) -> None:
        super().__init__(service)

    @router.get("/", response_model=DataSourceSchema, status_code=status.HTTP_200_OK)
    async def get(self, id: UUID) -> DataSourceSchema:
        obj = self.service.get_by_id(id)
        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Object with ID `{id}` was not found.",
            )
        return obj

    @router.get("/all", response_model=None)
    async def get_all(self, skip: int, limit: int) -> list[DataSourceSchema]:
        return self.service.get_all(skip, limit)  # type: ignore

    @router.post(
        "/", response_model=DataSourceSchema, status_code=status.HTTP_201_CREATED
    )
    async def create(self, input: DataSourceDTO) -> DataSourceSchema:
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
    async def update(self, id: UUID, input: DataSourceDTO) -> DataSourceSchema:
        obj = self.service.update(id, input)

        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Object with ID `{id}` was not found.",
            )
        return obj

from uuid import UUID

from fastapi import APIRouter, Depends, UploadFile, status
from src.models.domain.data_source.data_source import DataSource
from src.schema.data_source_schema import (
    DataSourceCreateSchema,
    DataSourceSchema,
    DataSourceUpdateSchema,
)
from src.service.data_source_service import get_data_source_service, DataSourceService
from src.service.base_service import BaseService

serviceType = BaseService[
    DataSource, DataSourceCreateSchema, DataSourceUpdateSchema, DataSourceSchema, UUID
]
router = APIRouter(prefix="/data-sources", tags=["Data Sources"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get(
    id: UUID, service: serviceType = Depends(get_data_source_service)
) -> DataSourceSchema:
    obj = service.get_by_id(id)

    return obj


@router.post("/from-file", status_code=status.HTTP_200_OK)
async def create_from_file(
    file: UploadFile, service: DataSourceService = Depends(get_data_source_service)
) -> DataSourceSchema:
    obj = service.from_file_text(file)

    return obj


@router.get("/all")
async def get_all(
    skip: int,
    limit: int,
    service: serviceType = Depends(get_data_source_service),
) -> list[DataSourceSchema]:
    return service.get_all(skip, limit)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(
    input: DataSourceCreateSchema,
    service: serviceType = Depends(get_data_source_service),
) -> DataSourceSchema:
    return service.create(input)


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete(
    id: UUID,
    service: serviceType = Depends(get_data_source_service),
):
    return service.delete(id)


@router.patch("/", status_code=status.HTTP_200_OK)
async def update(
    id: UUID,
    input: DataSourceUpdateSchema,
    service: serviceType = Depends(get_data_source_service),
) -> DataSourceSchema:
    obj = service.update(id, input)
    return obj

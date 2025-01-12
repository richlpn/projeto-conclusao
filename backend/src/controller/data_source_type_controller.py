from uuid import UUID

from fastapi import APIRouter, Depends, status
from src.models.data_source.data_source_type import DataSourceType
from src.schema.data_source_type_schema import (
    DataSourceTypeCreateSchema,
    DataSourceTypeSchema,
    DataSourceTypeUpdateSchema,
)
from src.service.base_service import BaseService
from src.service.data_source_type_service import get_data_source_type_service

serviceType = BaseService[
    DataSourceType,
    DataSourceTypeCreateSchema,
    DataSourceTypeUpdateSchema,
    DataSourceTypeSchema,
    UUID,
]
router = APIRouter(prefix="/data-source-type", tags=["Data Sources Type"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get(
    id: UUID, service: serviceType = Depends(get_data_source_type_service)
) -> DataSourceTypeSchema:
    obj = service.get_by_id(id)

    return obj


@router.get("/all")
async def get_all(
    skip: int,
    limit: int,
    service: serviceType = Depends(get_data_source_type_service),
) -> list[DataSourceTypeSchema]:
    return service.get_all(skip, limit)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(
    input: DataSourceTypeCreateSchema,
    service: serviceType = Depends(get_data_source_type_service),
) -> DataSourceTypeSchema:
    return service.create(input)


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete(
    id: UUID,
    service: serviceType = Depends(get_data_source_type_service),
):
    return service.delete(id)


@router.patch("/", status_code=status.HTTP_200_OK)
async def update(
    id: UUID,
    input: DataSourceTypeUpdateSchema,
    service: serviceType = Depends(get_data_source_type_service),
) -> DataSourceTypeSchema:
    obj = service.update(id, input)
    return obj

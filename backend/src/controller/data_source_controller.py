from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.schema.data_source_schema import (
    DataSource,
    DataSourceCreateSchema,
    DataSourceUpdateSchema,
)
from src.service.data_source_service import get_data_source_service
from src.utils.base_service import BaseService

serviceType = BaseService[
    DataSource, DataSourceCreateSchema, DataSourceUpdateSchema, UUID
]
router = APIRouter(prefix="/data-sources", tags=["Data Sources"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get(id: UUID, service: serviceType = Depends(get_data_source_service)):
    obj = service.get_by_id(id)

    return obj


@router.get("/all", response_model=None)
async def get_all(
    skip: int,
    limit: int,
    service: serviceType = Depends(get_data_source_service),
) -> list[DataSource]:
    l = service.get_all(skip, limit)
    return l


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(
    input: DataSourceCreateSchema,
    service: serviceType = Depends(get_data_source_service),
):
    return service.create(input)


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete(
    id: UUID,
    service: serviceType = Depends(get_data_source_service),
):

    obj = service.delete(id)


@router.patch("/", status_code=status.HTTP_200_OK)
async def update(
    id: UUID,
    input: DataSourceUpdateSchema,
    service: serviceType = Depends(get_data_source_service),
):
    obj = service.update(id, input)
    return obj

from uuid import UUID

from fastapi import APIRouter, Depends, status
from src.models.domain.data_source.data_source_column import DataSourceColumn
from src.schema.data_source_column_schema import (
    DataSourceColumnCreateSchema,
    DataSourceColumnSchema,
    DataSourceColumnUpdateSchema,
)
from src.service.data_source_column_service import (
    DataSourceColumnService,
    get_data_source_column_service,
)
from src.service.base_service import BaseService

serviceType = BaseService[
    DataSourceColumn,
    DataSourceColumnCreateSchema,
    DataSourceColumnUpdateSchema,
    DataSourceColumnSchema,
    UUID,
]
router = APIRouter(prefix="/data-source-columns", tags=["Data Source Columns"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get(
    id: UUID, service: serviceType = Depends(get_data_source_column_service)
) -> DataSourceColumnSchema:
    obj = service.get_by_id(id)
    return obj


@router.get("/all")
async def get_all(
    skip: int,
    limit: int,
    service: serviceType = Depends(get_data_source_column_service),
) -> list[DataSourceColumnSchema]:
    return service.get_all(skip, limit)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(
    input: DataSourceColumnCreateSchema,
    service: serviceType = Depends(get_data_source_column_service),
) -> DataSourceColumnSchema:
    return service.create(input)


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete(
    id: UUID,
    service: serviceType = Depends(get_data_source_column_service),
):
    return service.delete(id)


@router.patch("/", status_code=status.HTTP_200_OK)
async def update(
    id: UUID,
    input: DataSourceColumnUpdateSchema,
    service: serviceType = Depends(get_data_source_column_service),
) -> DataSourceColumnSchema:
    obj = service.update(id, input)
    return obj


@router.get("/data-source/", status_code=status.HTTP_200_OK)
async def get_by_data_source_id(
    data_source_id: UUID,
    service: DataSourceColumnService = Depends(get_data_source_column_service),
) -> list[DataSourceColumnSchema]:
    """
    Gets all DataSourceColumns associated with a given DataSource id.

    Args:
    - data_source_id (UUID): The id of the DataSource.

    Returns:
    - list[DataSourceColumnSchema]: A list of DataSourceColumnSchema objects.
    """
    return service.find_all_by_data_source_id(data_source_id)

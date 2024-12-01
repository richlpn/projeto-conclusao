from fastapi import APIRouter, Depends, status
from src.models.domain.requirements.requirement import Requirement
from src.schema.requirement_schema import (
    UUID,
    RequirementCreateSchema,
    RequirementSchema,
    RequirementUpdateSchema,
)
from src.service.requirement_service import get_requirement_service
from src.service.base_service import BaseService

router = APIRouter(prefix="/requirement", tags=["Data Sources Requirements"])

ServiceType = BaseService[
    Requirement,
    RequirementCreateSchema,
    RequirementUpdateSchema,
    RequirementSchema,
    UUID,
]


@router.get("/", status_code=status.HTTP_200_OK)
async def get(id: UUID, service: ServiceType = Depends(get_requirement_service)):
    obj = service.get_by_id(id)
    return obj


@router.get("/all", response_model=list[RequirementSchema])
async def get_all(
    skip: int, limit: int, service: ServiceType = Depends(get_requirement_service)
):
    return service.get_all(skip, limit)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=RequirementSchema)
async def create(
    input: RequirementCreateSchema,
    service: ServiceType = Depends(get_requirement_service),
):
    c = service.create(input)
    return c


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete(id: UUID, service: ServiceType = Depends(get_requirement_service)):
    obj = service.delete(id)


@router.patch("/", response_model=RequirementSchema, status_code=status.HTTP_200_OK)
async def update(
    id: UUID,
    input: RequirementUpdateSchema,
    service: ServiceType = Depends(get_requirement_service),
):
    obj = service.update(id, input)
    return obj

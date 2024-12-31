from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from src.models.domain.requirements.requirement import Requirement
from src.schema.requirement_schema import (
    UUID,
    RequirementCreateFromLLMSchema,
    RequirementSchema,
    RequirementUpdateSchema,
)
from src.service.requirement_service import RequirementService, get_requirement_service
from src.service.base_service import BaseService

router = APIRouter(prefix="/requirement", tags=["Data Sources Requirements"])

ServiceType = BaseService[
    Requirement,
    RequirementCreateFromLLMSchema,
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
    input: RequirementCreateFromLLMSchema,
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


@router.post("/from-data-source", status_code=status.HTTP_200_OK)
async def from_data_source(
    data_source_id: UUID, service: RequirementService = Depends(get_requirement_service)
):
    # try:
    return service.gen_from_data_source(data_source_id=data_source_id)
    # except ValidationError as err:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail=f"Error while parsing the schema.{err}",
    #     )

from uuid import UUID
from fastapi import APIRouter, Depends
from src.models.domain.requirements.task import Task
from src.service.task_service import get_task_service
from src.schema.task_schema import TaskCreateSchema, TaskSchema, TaskUpdateSchema
from src.service.base_service import BaseService

router = APIRouter(prefix="/tasks", tags=["Tasks"])


ServiceType = BaseService[
    Task,
    TaskCreateSchema,
    TaskUpdateSchema,
    TaskSchema,
    UUID,
]


@router.get("/all")
async def get(service: ServiceType = Depends(get_task_service)):
    return service.get_all()


@router.get("/")
async def read_task(task_id: UUID, service: ServiceType = Depends(get_task_service)):
    return service.get_by_id(task_id)


@router.post("/", status_code=201)
async def create_task(
    task: TaskCreateSchema, service: ServiceType = Depends(get_task_service)
):
    return service.create(task)


@router.patch("/", status_code=202)
async def update_task(
    task_id: UUID,
    task: TaskUpdateSchema,
    service: ServiceType = Depends(get_task_service),
):
    return service.update(task_id, task)


@router.delete("/")
async def delete_task(task_id: UUID, service: ServiceType = Depends(get_task_service)):
    service.delete(task_id)


@router.post("/generate", status_code=201)
async def generate_tasks(data_source_id: UUID, service=Depends(get_task_service)):
    # This type hint was removed to avoid the linting error regarding undefined function 'gen_from_data_source'.
    return service.gen_from_data_source(data_source_id)


@router.get("/data-source", status_code=200)
async def from_data_source(id: UUID, service=Depends(get_task_service)):
    # This type hint was removed to avoid the linting error regarding undefined function 'get_from_data_source'.
    return service.get_from_data_source(id)

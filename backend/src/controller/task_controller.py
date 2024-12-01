from uuid import UUID
from fastapi import APIRouter, Depends
from src.models.domain.requirements.task import Task
from src.service.task_service import get_task_service
from src.schema.task_schema import TaskCreateSchema, TaskSchema, TaskUpdateSchema
from src.utils.base_service import BaseService

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


@router.post("/")
async def create_task(
    task: TaskCreateSchema, service: ServiceType = Depends(get_task_service)
):
    return service.create(task)


@router.put("/")
async def update_task(
    task_id: UUID,
    task: TaskUpdateSchema,
    service: ServiceType = Depends(get_task_service),
):
    return service.update(task_id, task)


@router.delete("/")
async def delete_task(task_id: UUID, service: ServiceType = Depends(get_task_service)):
    service.delete(task_id)

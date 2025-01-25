from uuid import UUID
from fastapi import APIRouter, status, Depends
from src.service.script_generation_service import get_script_generation_service


router = APIRouter(prefix="/script", tags=["Script Generation"])


@router.post("/script", status_code=status.HTTP_201_CREATED)
async def generate_script(
    data_source_id: UUID,
    service=Depends(get_script_generation_service),
) -> str:
    return service.create(data_source_id)

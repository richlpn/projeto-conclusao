from fastapi import APIRouter, HTTPException, status
from pydantic import ValidationError
from src.config.controller import controller
from src.config.dependency_injection import autowired
from src.models.domain.requirement import Requirement
from src.models.dtos.requirements_dto import BaseDTO, RequirementDTO
from src.schema.requirement_schema import BaseSchema, Requirement, UUID
from src.utils.base_controller import BaseController
from src.utils.base_service import BaseService

router = APIRouter(prefix="/requirement", tags=["Data Sources Requirements"])


@controller(router)
class RequirementController(
    BaseController[
        BaseService[Requirement, BaseDTO[Requirement], UUID],
        BaseDTO[Requirement],
        BaseSchema[Requirement],
        UUID,
    ]
):
    @autowired
    def __init__(
        self, service: BaseService[Requirement, BaseDTO[Requirement], UUID]
    ) -> None:
        super().__init__(service)

    @router.get("/", status_code=status.HTTP_200_OK)
    async def get(self, id: UUID, *args, **kwargs) -> BaseSchema[Requirement]:
        obj = self.service.get_by_id(id)
        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Object with ID `{id}` was not found.",
            )
        return obj

    @router.get("/all", response_model=None)
    async def get_all(
        self, skip: int, limit: int, *args, **kwargs
    ) -> list[BaseSchema[Requirement]]:
        return self.service.get_all(skip, limit)  # type: ignore

    @router.post("/", status_code=status.HTTP_201_CREATED)
    async def create(self, input: RequirementDTO) -> BaseSchema[Requirement]:
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
    async def update(self, id: UUID, input: RequirementDTO) -> BaseSchema[Requirement]:
        obj = self.service.update(id, input)

        if obj is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Object with ID `{id}` was not found.",
            )
        return obj

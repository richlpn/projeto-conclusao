from pydantic import Field
from src.models.domain.data_source.data_source import DataSource
from src.models.dtos.base_dto import BaseDTO


class DataSourceColumnDTO(BaseDTO[DataSource]):
    type: str = Field(description="Column type.")
    name: str = Field(description="Column name.")
    description: str = Field(description="Column brief description (used for context)")

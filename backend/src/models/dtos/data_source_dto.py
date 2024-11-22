from pydantic import Field, BaseModel
from typing import Optional

from src.models.domain.data_source.data_source import DataSourceType
from src.models.dtos.data_source_column_dto import DataSourceColumnDTO


class DataSourceDTO(BaseModel):
    """
    Data Transfer Object for the DataSource class.
    """

    name: str
    type: DataSourceType = Field()
    columns: list[DataSourceColumnDTO] = Field(default_factory=list)
    separator: str | None = Field(default=None)

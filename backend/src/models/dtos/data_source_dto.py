from pydantic import Field

from src.models.domain.data_source.data_source import DataSource, DataSourceType
from src.models.dtos.data_source_column_dto import DataSourceColumnDTO
from src.schema.data_source_schema import DataSourceSchema
from src.models.dtos.base_dto import BaseDTO


class DataSourceDTO(BaseDTO[DataSource]):
    """
    Data Transfer Object for the DataSource class.
    """

    __model__ = DataSource
    name: str
    type: DataSourceType = Field()
    columns: list[DataSourceColumnDTO] = Field(default_factory=list)
    separator: str | None = Field(default=None)

import uuid
from pydantic import Field
from src.models.domain.data_source.data_source_column import DataSourceColumn
from src.utils.base_schema import BaseSchema


class DataSourceColumnSchema(BaseSchema[DataSourceColumn]):
    id: uuid.UUID = Field(description="Unique Indentifier")
    type: str = Field(description="Column type.")
    name: str = Field(description="Column name.")
    description: str = Field(description="Column brief description (used for context)")

    @classmethod
    def from_model(cls, model: DataSourceColumn) -> BaseSchema[DataSourceColumn]:
        return DataSourceColumnSchema(
            id=model.id,  # type: ignore
            type=model.type,  # type: ignore
            name=model.name,  # type: ignore
            description=model.description,  # type: ignore
        )

    def to_model(self) -> DataSourceColumn:
        return DataSourceColumn(
            id=self.id,  # type: ignore
            type=self.type,  # type: ignore
            name=self.name,  # type: ignore
            description=self.description,  # type: ignore
        )

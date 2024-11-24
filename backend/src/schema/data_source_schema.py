import uuid
from pydantic import Field
from src.models.domain.data_source.data_source import DataSource, DataSourceType
from src.schema.data_source_column_schema import DataSourceColumnSchema
from src.utils.base_schema import BaseSchema


class DataSourceSchema(BaseSchema[DataSource]):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str = Field(description="Data Source Name")
    type: DataSourceType = Field(description="Type of the data source.")
    columns: list[DataSourceColumnSchema] = Field(
        default_factory=list, description="Columns used or referenced on the table."
    )
    separator: str | None = Field(
        default=None,
        description="Separator used only to describe the sperator of a CSV. If not informed must be set to None",
    )

    def to_model(self) -> DataSource:

        columns = [col_schema.to_model() for col_schema in self.columns]
        return DataSource(
            id=self.id,
            name=self.name,
            type=self.type,
            columns=columns,
            separator=self.separator,
        )

    @classmethod
    def from_model(cls, model: DataSource) -> BaseSchema[DataSource]:
        return cls(
            id=model.id,  # type: ignore
            name=model.name,  # type: ignore
            type=model.type,  # type: ignore
            columns=[col.from_model(col) for col in model.columns],  # type: ignore
            separator=model.separator,  # type: ignore
        )

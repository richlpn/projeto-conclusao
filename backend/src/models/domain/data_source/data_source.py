import uuid
import enum
from pydantic import BaseModel, Field
from sqlalchemy import Column, Enum, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.utils.database import Base
from .data_source_column import DataSourceColumn


class DataSourceType(str, enum.Enum):
    CSV = "csv"
    SQL = "sql"
    XLSX = "xlsx"
    JSON = "json"


class DataSource(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str = Field(description="Data Source Name")
    type: DataSourceType = Field(description="Type of the data source.")
    columns: list[DataSourceColumn] = Field(
        default_factory=list, description="Columns used or referenced on the table."
    )
    separator: str | None = Field(
        default=None,
        description="Separator used only to describe the sperator of a CSV. If not informed must be set to None",
    )

    class model_schema(Base):
        __tablename__ = "data_sources"

        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        name = Column(String)
        type = Column(Enum(DataSourceType))
        separator = Column(String, nullable=True)

        columns = relationship("DataSourceColumnSchema")

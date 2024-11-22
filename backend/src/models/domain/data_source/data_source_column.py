"""
Module containing Pydantic models for data documentation schemas.

These models define the structure and validation rules for data documentation,
including data sources, tables, columns, and data transformation operations.

The models in this module are used to validate and parse data documentation
schemas, ensuring that they conform to a standard format and contain the
required information.

Classes:
    ColumnSchema: Represents a column in a table, including its type, name, and description.
    DataSourceType: An enumeration of supported data source types (e.g., CSV, SQL, XLSX, JSON).
    TableSchema: Represents a table in a data source, including its type, name, columns, and separator.
    DataSourceSchema: Represents a data source, including its name, tables, and data transformation operations.

See Also:
    src.models.operations: Module containing Pydantic models for data transformation operations.
"""

import uuid

from pydantic import BaseModel, Field
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.utils.database import Base


class DataSourceColumn(BaseModel):
    id: uuid.UUID = Field(description="Unique Indentifier")
    type: str = Field(description="Column type.")
    name: str = Field(description="Column name.")
    description: str = Field(description="Column brief description (used for context)")

    # Define the ColumnSchema table
    class data_schema(Base):
        __tablename__ = "column_schemas"

        id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
        type = Column(String, default="str")
        name = Column(String, default="str")
        description = Column(String)

        data_source_id = Column(UUID(as_uuid=True), ForeignKey("data_sources.id"))
        data_source = relationship("DataSource", back_populates="columns")

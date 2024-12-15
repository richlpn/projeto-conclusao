import uuid
import enum
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.config.database import Base


class DataSource(Base):
    """
    Represents a data source in the database.

    A data source is a collection of data that can be used for analysis or processing.
    It can be a file, a database table, or any other type of data storage.

    Attributes:
        id (UUID): A unique identifier for the data source.
        name (str): The name of the data source.
        type (DataSourceType): The type of the data source (e.g. CSV, Excel, etc.).
        separator (str): The separator used in the data source (e.g. comma, semicolon, etc.).
        columns (list[DataSourceColumn]): A list of columns in the data source.

    Relationships:
        columns: A one-to-many relationship with the DataSourceColumn class.
    """

    __tablename__ = "data_sources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String)
    separator = Column(String, nullable=True)

    columns = relationship("DataSourceColumn", lazy="joined")
    requirement = relationship("Requirement", lazy="joined")
    type = relationship("DataSourceType", lazy="joined")
    type_id = Column(
        UUID(as_uuid=True), ForeignKey("data_source_type.id", ondelete="CASCADE")
    )

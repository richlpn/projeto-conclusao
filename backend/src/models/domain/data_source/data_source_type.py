import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from src.config.database import Base


class DataSourceType(Base):
    __tablename__ = "data_source_type"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String())
    data_source = relationship("DataSource", back_populates="columns")

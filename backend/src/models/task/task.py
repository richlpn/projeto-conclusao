from uuid import uuid4
from src.config.database import Base
from sqlalchemy import UUID, Column, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship


class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    signature_function = Column(String, nullable=False)

    data_source_id = Column(
        UUID(as_uuid=True), ForeignKey("data_sources.id", ondelete="CASCADE")
    )
    data_source = relationship("DataSource", back_populates="tasks")

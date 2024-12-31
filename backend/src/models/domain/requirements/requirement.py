from uuid import uuid4

from sqlalchemy import UUID, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import relationship
from src.config.database import Base


class Requirement(Base):
    __tablename__ = "requirements"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    tasks = relationship("Task", backref="Requirement", lazy="joined")

    data_source_id = Column(
    UUID(as_uuid=True), ForeignKey("data_sources.id", ondelete="CASCADE")
    )
    code = Column(TEXT, nullable=True)

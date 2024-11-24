from uuid import uuid4

from sqlalchemy import UUID, Column, ForeignKey, String
from sqlalchemy.orm import relationship
from src.config.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    signature_function = Column(String)

    requirement_id = Column(UUID(as_uuid=True), ForeignKey("requirements.id"))
    requirement = relationship("Requirement", back_populates="tasks")

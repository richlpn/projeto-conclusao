from uuid import uuid4
from src.config.database import Base
from sqlalchemy import UUID, Column, ForeignKey, String, Integer


class Task(Base):
    __tablename__ = "tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    signature_function = Column(String, nullable=False)

    requirement_id = Column(
        UUID(as_uuid=True), ForeignKey("requirements.id", ondelete="CASCADE")
    )

# task_model.py
from src.config.database import Base
from sqlalchemy import UUID, Column, ForeignKey, String, Integer


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    signature_function = Column(String, nullable=False)

    requirement_id = Column(UUID(as_uuid=True), ForeignKey("requirements.id"))

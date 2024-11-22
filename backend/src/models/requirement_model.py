from pydantic import BaseModel, Field


class Task(BaseModel):
    title: str = Field(description="A short descriptive title about the task")
    description: str = Field(
        description="A Detailed explanation of what must be executed on this task, containing inputs, ouputs and previous dependecies."
    )
    signature_function: str = Field(
        description="Name of the python signature function that must be implemented by the task."
    )

    def __str__(self) -> str:
        return f"Title: {self.title}\nDescription: {self.description}\n"


class Requirement(BaseModel):
    title: str = Field(description="Requirement title")
    tasks: list[Task] = Field(
        default_factory=list,
        description="List of task to be completed in order to fulfill this requirement.",
    )

from pydantic import BaseModel, Field


class Task(BaseModel):
    description: str = Field(..., description="The description of the task.")
    parameters: list[str] = Field(
        default_factory=list,
        description="A list of parameters to be used. Or considered when executing the task.",
    )
    subtasks: list["Task"] = Field(
        default_factory=list, description="Subtasks that combined solves a bigger task."
    )


class Requirement(BaseModel):
    title: str = Field(description="Requirement title")
    tasks: list[Task] = Field(default_factory=list)

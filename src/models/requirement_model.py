from pydantic import BaseModel, Field


class Task(BaseModel):
    title: str = Field(
        description="Task title",
        examples=[
            "TASK 1: Read Data Source",
            "TASK 5: Write the final dataframe to disk",
        ],
    )
    description: str = Field(
        description="The description of the task.",
        examples=[
            "Use the `SAILES_PATH` environment variable to get the path of the file.",
            "Create the function 'parse_columns' that takes a string and transforms then into sneak_case.",
            "Validate if the file on the path is a CSV. Raise an ValueError with message 'File extention not suported by this pipeline'.",
        ],
    )


class Requirement(BaseModel):
    title: str = Field(description="Requirement title")
    tasks: list[Task] = Field(
        default_factory=list,
        description="List of task to be completed in order to fulfill this requirement.",
    )

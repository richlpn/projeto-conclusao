from pydantic import RootModel, Field
from .join import JoinOperation
from .filter import FilterOperation
from .aggregate import AggregateOperation
from .transform import TransformOperation


class Operation(RootModel):
    root: JoinOperation | FilterOperation | AggregateOperation | TransformOperation = (
        Field(..., discriminator="type")
    )

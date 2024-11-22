from enum import Enum
from pydantic import BaseModel, Field


class ReviewStatus(Enum):
    APPROVED = "Approved"
    DENIED = "Denied"
    WAITING = "Waiting"


class Review(BaseModel):

    status: ReviewStatus = Field(
        default=ReviewStatus.WAITING, description="Status of the review"
    )
    description: str = Field(
        default="WAITING FOR REVIEW", description="Description of the review"
    )

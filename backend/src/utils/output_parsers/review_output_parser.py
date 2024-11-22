import re

from langchain_core.output_parsers.base import BaseOutputParser
from langchain_core.exceptions import OutputParserException

from src.models.review_model import Review, ReviewStatus
from src.utils.llm_logger import LOGGER


class ReviewOutputParser(BaseOutputParser[Review]):

    def parse(self, text: str) -> Review:
        status = re.search(r'"\w+"', text)
        if status is None:
            raise OutputParserException("Could not find review status")

        status = status.group()
        description = text.replace(f"REVIEW_STATUS={status}", "")

        status = status.replace('"', "")

        return Review(status=ReviewStatus(status), description=description)  # type: ignore

    def get_format_instructions(self) -> str:

        return f"""Your review must start with `REVIEW_STATUS="{ReviewStatus.APPROVED.value}"` or `REVIEW_STATUS="{ReviewStatus.DENIED.value}"`
        You're not allowed to write or re-write any code blocks."""

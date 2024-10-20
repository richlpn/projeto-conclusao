import os

from langchain.agents import tool
from langchain_community.document_loaders import TextLoader
from ..models.call_tools_model import ToolCallAnswer


@tool
def read_file_tool(path: str) -> ToolCallAnswer[str]:
    """
    Tool used to read any type of file documentations (e.g. .txt, .pdf).
    Args:
        path (str): Path to the file that you want to read.
    Returns:
        ToolCallAnswer: A tool call answer containing the text content of the file.
    """
    # check if the file exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"File {path} does not exist")

    # get the type of the file using the extention (e.g., .txt, .pdf, etc.)
    ext = path.split(".")[-1]

    if ext == "pdf":
        content = ""

    else:
        content = TextLoader(path, autodetect_encoding=True).load()[0].page_content

    return ToolCallAnswer[str](tool_name="read_file", input=path, output=content)

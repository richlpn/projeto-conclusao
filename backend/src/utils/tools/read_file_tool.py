import os

from langchain.agents import tool
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.utils.llm_logger import LOGGER
from ..graph.nodes.call_tools_model import ToolCallAnswer


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

    elif ext == "txt":
        with open(path, encoding="utf-8") as file:
            content = file.read()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_text(content)

    return ToolCallAnswer[list[str]](tool_name="read_file", input=path, output=texts)

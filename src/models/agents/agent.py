import os
from typing import Any, Generic, TypeVar

import msgspec
from langchain.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers.base import BaseOutputParser
from langchain_core.runnables import Runnable
from langchain_ollama import ChatOllama

P = TypeVar("P")
PROMPT_DIR = os.getenv("PROMPT_DIR")

if PROMPT_DIR is None:
    raise ValueError("Missing env variable `PROMPT_DIR`.")


class Agent(Runnable, Generic[P]):
    __prompt_dir__: str = PROMPT_DIR

    name: str
    model: Runnable[list, BaseMessage]
    prompt: ChatPromptTemplate
    parser: BaseOutputParser[P] | None = None
    tools: list[Runnable[list, BaseMessage]] | None = None
    temperature: float

    def __init__(self) -> None:
        self._filename = "".join(
            ["_" + i.lower() if i.isupper() else i for i in self.__class__.__name__]
        ).lstrip("_")

        dir = os.path.join(self.__prompt_dir__, f"{self._filename}.yml")

        with open(dir) as f:
            yml = msgspec.yaml.decode(f.read())["Agent"]

        self.name = yml["name"]
        self.temperature = yml.get("temperature", 0.8)
        self.model = self.__get_model__(yml)

        self.input_variables = yml["input_variables"]
        self.prompt = ChatPromptTemplate(
            messages=list(yml["prompts"].items()),
            input_variables=yml["input_variables"],
        )
        if self.tools:
            self.model = self.model.bind_tools(self.tools)  # type: ignore

        self.chain = self.prompt | self.model
        if self.parser:
            self.chain = self.chain | self.parser

    def __get_model__(self, yml: dict[str, Any]) -> BaseLanguageModel:

        model_source = yml["model"].get("source")
        if not model_source:
            return ChatOllama(model=yml["model"], temperature=self.temperature)

        if model_source == "anthropic":
            return ChatAnthropic(
                model=yml["model"]["name"], temperature=self.temperature
            )  # type: ignore

        if model_source == "ollama":
            return ChatOllama(model=yml["model"]["name"], temperature=self.temperature)

        raise ValueError(f"{model_source} is not a supported model source")

    def invoke(self, **kwargs) -> P:
        call = {**kwargs}
        if self.parser:
            call["PARSER"] = self.parser.get_format_instructions()

        res = self.chain.invoke(call)
        return res  # type: ignore

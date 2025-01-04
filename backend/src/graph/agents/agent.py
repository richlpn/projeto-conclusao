import os
from typing import Any, Generic, TypeVar

import yaml
from langchain.prompts import ChatPromptTemplate
from langchain_anthropic import ChatAnthropic
from langchain_community.chat_models.sambanova import ChatSambaNovaCloud
from langchain_core.language_models.base import BaseLanguageModel
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers.base import BaseOutputParser
from langchain_core.runnables import Runnable
from langchain_ollama import ChatOllama
from src.config import get_settings

settings = get_settings()
P = TypeVar("P")


class Agent(Runnable, Generic[P]):
    __prompt_dir__: str = settings.prompts

    llm_name: str
    model: Runnable[list, BaseMessage]
    prompt: ChatPromptTemplate
    parser: BaseOutputParser[P] | None = None
    tools: list[Runnable[list, BaseMessage]] | None = None
    temperature: float

    def __load_config__(self):
        self._filename = "".join(
            ["_" + i.lower() if i.isupper() else i for i in self.__class__.__name__]
        ).lstrip("_")

        dir = os.path.join(self.__prompt_dir__, f"{self._filename}.yml")

        with open(dir, "r") as f:
            yml = yaml.safe_load(f)["Agent"]

        return yml

    def __set_params__(self, yml: dict):
        self.llm_name = yml["name"]
        self.temperature = yml.get("temperature", 0.8)

        self.prompt = ChatPromptTemplate(
            messages=list(yml["prompts"].items()),
            input_variables=yml["input_variables"],
        )

    def __create_chain__(self):
        if self.model is None or self.prompt is None:
            raise ValueError("Missing `model` or `prompt`.")

        if self.tools:
            self.model = self.model.bind_tools(self.tools)  # type: ignore

        self.chain = self.prompt | self.model
        if self.parser:
            self.chain = self.chain | self.parser

    def __init__(self) -> None:

        config = self.__load_config__()
        self.__set_params__(config)
        self.model = self.__get_model__(config)
        self.__create_chain__()

    def __get_model__(self, yml: dict[str, Any]) -> BaseLanguageModel:

        model_source = yml["model"]
        if isinstance(model_source, str):
            return ChatOllama(model=yml["model"], temperature=self.temperature)

        if model_source["source"] == "anthropic":
            return ChatAnthropic(
                model_name=yml["model"]["name"], temperature=self.temperature
            )  # type: ignore

        if model_source["source"] == "ollama":
            return ChatOllama(model=yml["model"]["name"], temperature=self.temperature)

        if model_source["source"] == "sambanova":
            return ChatSambaNovaCloud(
                model=yml["model"]["name"], temperature=self.temperature
            )

        raise ValueError(f"{model_source} is not a supported model source")

    def invoke(self, *args, **kwargs) -> P:
        call = {**kwargs}
        if self.parser:
            call["PARSER"] = self.parser.get_format_instructions()

        res = self.chain.invoke(call)
        return res  # type: ignore


from typing import Any
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_core.runnables import Runnable
from output_parsers.codeblock_output_parser import PythonCodeParser
from models.graph import GraphState

class Engineer(Runnable):

    DEV_TOOLS:list[str] = ['Python3.11', 'Pandas', 
                                 'bibliotecas padrão python', 
                                 'Bibliotecas de conexão há bancos de dados (psycopg2, etc)']
    
    role_prompt: tuple[str, str] = (
        "system",
        """Aja como um engenheiro de dados especialista na etapa de extração de dados.
        O analísta de dados vai te informar um conjunto de informações sobre uma fonta de dados em formato JSON.
        Sua tarefa é criar um script para fazer a extração para a fonte de dados informada.
        As tecnologias de desenvolvimento disponíveis são {tools}.
        caso você tenha finalizado a sua tarefa ou não for possivel realizar qualquer ação, envie uma mensagem dizendo apenas 'MEU TRABALHO FOI FINALIZADO'.
        {output_parser}"""
        )

    _parser = PythonCodeParser()
    

    @tool
    def determinar_separador(self, file_path:str, sample_size:int) -> str:
        """Utiliza o caminho do arquivo e um tamanho da amostra fornecidos pelo analista no schema da fonte de dados."""

        print("EXTRACTION AGENT: Finding separator")

        SEPARATORS = {'|': 0, ',':0, ';':0}
        file = open(file_path, 'r')
        content = ''.join(file.readlines(sample_size))
        file.close()
        for char in content:
            if char in SEPARATORS:
                SEPARATORS[char] += 1
        sep = max(SEPARATORS, key=lambda x: SEPARATORS[x])

        print(f"EXTRACTION AGENT: Found separator '{sep}'")
        return sep
    
    @tool
    def gerar_script_extracao(self, extraction_steps: str) -> str:
        """Utiliza o json fornecido pelo analista para gerar um script utilizando de extração da fonte de dados. retorna o script em forma de texo"""
        print("EXTRACTION AGENT: Generating script")
        
        prompt = f"""
        Siga o paradigma funcional e as melhores práticas de desenvolvimento de software.
        A primeira linha do script gerado deve ser um comentário com o nome do script no seguinte padrão: 'raw_<nome_script'.py
        {extraction_steps}"""

        self.response = self.chain.invoke({'ordem_lider':prompt})

        print(f"EXTRACTION AGENT: Script generated succefully. Output Size = {len(self.response)}")
        return self.response
    
    def __init__(self, model: BaseChatModel) -> None:
        self.prompt = (
            ChatPromptTemplate([self.role_prompt, MessagesPlaceholder(variable_name='ordem_lider')])
            .partial(output_parser=self._parser.get_format_instructions())
            .partial(tools=','.join(self.DEV_TOOLS)))
        
        self.tools = [self.determinar_separador, self.gerar_script_extracao]
        self.agent = model.bind_tools(self.tools)
        self.chain = self.prompt | model | self._parser

    def invoke(self, state: GraphState,  **karg) -> BaseMessage:
        return self(state)

    def __call__(self, state: GraphState) -> BaseMessage:
           self._response = self.chain.invoke(state) # type: ignore
           
           return self._response
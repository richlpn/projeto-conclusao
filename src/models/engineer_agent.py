
from typing import Any
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_core.runnables import Runnable
from output_parsers.codeblock_output_parser import PythonCodeParser
from models.graph import END_CALL_LOOP, GraphState

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
        caso você tenha finalizado a sua tarefa ou um erro ocorra responda com {end_call}."""
        )

    _parser = PythonCodeParser()
    
    name:str = 'Engenheiro de dados'
    
    def create_sep_tool(self) -> Runnable:
        
        @tool
        def determinar_separador(file_path:str, sample_size:int) -> str:
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
        return determinar_separador # type: ignore
    
    def create_gen_script(self, model:BaseChatModel) -> Runnable:
                   
        prompt = ChatPromptTemplate.from_messages([
            ('system',"""Siga o paradigma funcional e as melhores práticas de desenvolvimento de software.
            {output_parser}
            A primeira linha do script gerado deve ser um comentário com o nome do script no seguinte padrão: 'raw_<nome_script'.py"""),
            MessagesPlaceholder('{extraction_steps}')
        ]).partial(output_parser=self._parser.get_format_instructions())

        chain = prompt | model | self._parser

        @tool
        def gerar_script_extracao(extraction_steps: str) -> str:
            """Utiliza um conjunto de especificações e detalhes sobre uma fonte de dados para retorna um script de extração dessa fonte.
            Args:
                extraction_steps (str): Json fornecido pelo analista com detalhes sobre o script gerado""" 
            response = chain.invoke({'extraction_steps':extraction_steps})
            return response
        
        return gerar_script_extracao # type: ignore
    
    def __init__(self, model: BaseChatModel) -> None:
        self.prompt = (
            ChatPromptTemplate([self.role_prompt, MessagesPlaceholder(variable_name='messages')])
            .partial(end_call=END_CALL_LOOP)
            .partial(tools=','.join(self.DEV_TOOLS)))
        
        self.tools = [self.create_gen_script(model), self.create_sep_tool()]
        self.agent = model.bind_tools(self.tools, tool_choice='any') # type: ignore
        self.chain = self.prompt | self.agent

    def invoke(self, state: GraphState,  **karg) -> BaseMessage:
        self._response = self.chain.invoke(state) # type: ignore
           
        return self._response
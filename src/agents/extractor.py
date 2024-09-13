from typing_extensions import Unpack
from pydantic import BaseModel, ConfigDict, Field
from langchain_core.prompts import PromptTemplate
from random import randint, seed

seed('1239092039')


class ExtractorSchema(BaseModel):
    _taskId: int
    sourceType:str = Field(description='Tipo da fonte de dados (por exemplo, "SQL", "CSV", "XLSX"). String, conjunto predefinido de valores.')
    connectionDetails:str|dict[str,str] = Field(description='Informações de conexão para a fonte de dados. Objeto, estrutura varia de acordo com o sourceType.')
    extractionDetails:str = Field(description='Nome da tabela caso sourceType seja "SQL", caso contrário caminho do(s) arquivo para extração de dados')
    tableName:str|None = Field(description='Nome da tabela a ser extraída (para fontes SQL). String, máximo 100 caracteres.')
    columns:list[str] = Field(description='Lista de colunas a serem extraídas. Array de strings, máximo 100 colunas.')
    conditions:str|None = Field(description='Condições e limitações para filtrar os dados durante a extração. Ex. Primeiros 100000 de registros. Ex ID >= 20')
    outputFormat:str = Field(description='Formato dos dados extraídos (por exemplo, "SQL", "CSV", "XLSX"). String, conjunto predefinido de valores.')
    outputName:str = Field(description='Nome da tabela ou arquivo (caminho) para carregar o resultado seguindo o padrão snake case.')
    def model_post_init(self, *args):
        self._taskId = randint(0, 9999999999999)

class Extractor:
    
    def __init__(self, model) -> None:
        self._prompt = PromptTemplate(
            template='Aja como especialista em engenharia de pipeline de dados, sua tarefa é escrever código python para fazer a etapa de extração de uma ou multiplas fontes de dados. As informações a seguir descrevem as caracteristicas e limitações da fonte de dados, Sua tarefa é escrever somente o código necessário para fazer a extração da fonte de dados seguindo as melhores práticas de desenvolvimento de software e otimização, apenas as bibliotecas {libraries} estão Disponíveis:\n{extraction_steps}',
            input_variables=["extraction"],
            partial_variables={"libraries": ['Pandas', 'bibliotecas padrão python']}
        )

        self._chain = self._prompt | model 

    def invoke(self, extraction: ExtractorSchema) -> str:
        """returns the code block"""
        self.response = self._chain.invoke(extraction)

        return self.response

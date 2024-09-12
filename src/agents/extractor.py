from typing_extensions import Unpack
from pydantic import BaseModel, ConfigDict, Field

from random import randint, seed

seed('1239092039')


class ExtractorSchema(BaseModel):
    _taskId: int
    sourceType:str = Field(description='Tipo da fonte de dados (por exemplo, "SQL", "CSV", "XLSX"). String, conjunto predefinido de valores.')
    connectionDetails:str = Field(description='Informações de conexão para a fonte de dados. Objeto, estrutura varia de acordo com o sourceType.')
    extractionDetails:str|dict[str,str] = Field(description='Caminho do arquivo para extração de dados ou credências de autenticação')
    tableName:str|None = Field(description='Nome da tabela a ser extraída (para fontes SQL). String, máximo 100 caracteres.')
    columns:str = Field(description='Lista de colunas a serem extraídas. Array de strings, máximo 100 colunas.')
    conditions:str = Field(description='Condições e limitações para filtrar os dados durante a extração. Ex. Primeiros 100000 de registros. Ex ID >= 20')
    outputFormat:str = Field(description='Formato dos dados extraídos. String, conjunto predefinido de valores.')

    def model_post_init(self, *args):
        self._taskId = randint(0, 9999999999999)

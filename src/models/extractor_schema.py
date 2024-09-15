
from pydantic import BaseModel, Field
from random import randint, seed


seed('1239092039')
# TODO: Better output format structure including: OutputType (SQL == Table), OutputConnectionDetails

class ExtractorSchema(BaseModel):
    _taskId: int
    sourceType:str = Field(description='Tipo da fonte de dados (por exemplo, "SQL", "CSV", "XLSX"). String, conjunto predefinido de valores.')
    connectionDetails:dict[str,str] = Field(default_factory=dict, description='Informações de conexão para a fonte de dados. Objeto, estrutura varia de acordo com o sourceType.')
    extractionDetails:dict[str,str] = Field(default_factory=dict, description='Nome da tabela caso sourceType seja "SQL". Para outros arquivos deve conter o caminho')
    tableName:str|None = Field(description='Nome da tabela a ser extraída (para fontes SQL). String, máximo 100 caracteres.')
    columns:list[str] = Field(description='Lista de colunas a serem extraídas. Array de strings, máximo 100 colunas.')
    conditions:str|None = Field(description='Condições e limitações para filtrar os dados durante a extração. Ex. Primeiros 100000 de registros. Ex ID >= 20')
    outputDetails:dict[str,str] = Field(description='Dicionário contendo informações sobre persistencia da extração, formato (Tabela SQL, CSV, XLSX), local de persistencia (Credencias de acesso ao banco ou caminho para escrita do arquivo)')
    outputName:str = Field(description='Nome da tabela ou arquivo (caminho) para carregar o resultado seguindo o padrão snake case.')

    def model_post_init(self, *args):
        self._taskId = randint(0, 9999999999999)

        if self.sourceType == 'CSV':
            self.connectionDetails = {
                **self.connectionDetails,
                'detectSeparator': 'True',
                'sampleSize': '1000'
            }

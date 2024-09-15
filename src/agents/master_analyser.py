from typing import Any
from langchain_core.tools import tool, ToolException
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.language_models import BaseChatModel
from langchain_core.runnables import Runnable
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.messages import BaseMessage

from models.extractor_schema import ExtractorSchema
from models.graph import GraphState

documentation = """Agência Nacional de Telecomunicações – Anatel

Metadados Principais
Título da base de dados: Arrecadação - Valores de Tributos e Preços Públicos
Descrição: O glossário descreve os dados disponíveis na base de dados “Arrecadação - Valores de Tributos e Preços Públicos” referentes à Contribuição para o Fomento da Radiodifusão Pública – CFRP, Taxa de Fiscalização de Instalação – TFI, Taxa de Fiscalização de Funcionamento – TFF, Preço Público pelo Direito de Uso de Radiofrequências – PPDUR, Preço Público pelo Direito de Exploração de Serviços de Telecomunicações e de Satélite – PPDESS.
Palavras-Chave: Anatel, CFRP, TFF, TFI, PPDESS, PPDUR.
Autor: Agência Nacional de Telecomunicações - Anatel
Área Técnica Responsável: Gerência de Finanças, Orçamento e Arrecadação – AFFO
E-mail da área técnica: affo5@anatel.gov.br
Periodicidade da Atualização: Mensal
Temas aos quais o dado está associado: Arrecadação e Telecomunicações
Glossário de Termos
Arquivo Taxas_Estacoes.csv
Numservico: código numérico identificador do Serviço de Telecomunicação.
NomeServico: nome do Serviço de Telecomunicação. Serviço de telecomunicação é o conjunto de atividades que possibilita a oferta de telecomunicação. Telecomunicação é a transmissão, emissão ou recepção, por fio, radioeletricidade, meios ópticos ou qualquer outro processo eletromagnético, de símbolos, caracteres, sinais, escritos, imagens, sons ou informações de qualquer natureza. (conforme Art. 60 da Lei 9.472/1997)
CodReceita: código numérico identificador da receita produto da arrecadação das taxas, contribuição e preços públicos.
SiglaReceita: sigla da receita, sendo: TFI - Taxa de Fiscalização de Instalação; TFI-SAT - Taxa de Fiscalização de Instalação - Satélite; TFF - Taxa de Fiscalização de Funcionamento; TFF-SAT - Taxa de Fiscalização de Funcionamento - Satélite; CFRP - Contribuição para o Fomento da Radiodifusão Pública.
codEstacaoDebito: código alfabético identificador do tipo de estação de telecomunicações relacionado ao respectivo serviço de telecomunicação. Estação de telecomunicações é o conjunto de equipamentos ou aparelhos, dispositivos e demais meios necessários à realização de telecomunicação, seus acessórios e periféricos, e, quando for o caso, as instalações que os abrigam e complementam, inclusive terminais portáteis. (conforme Art. 60 da Lei 9.472/1997)
ValorBase: valor unitário por estação relativo à receita e ao serviço de telecomunicações.
DescCodEstacaoDebito: descritivo da estação de telecomunicações e suas características distintivas.
Persistencia: A base deve ser persistida em uma tabela no banco postgresql://user:pass@localhost/mydatabase
"""

class Analist(Runnable):
    role_prompt:tuple[str,str] = (
    "system",
    """Você é um especialista em analise de dados e na gestão de fontes de dados.
    Seu trabalho é apoiar o engenheiro de dados, utilizando as seguintes ferramentas.
    caso você tenha finalizado a sua tarefa ou não for possivel realizar qualquer ação, envie uma mensagem dizendo apenas 'PIPELINE FINALIZADA!'.
    {output_parser}""")

    parser = PydanticOutputParser(pydantic_object=ExtractorSchema)


    @tool
    def extrair_dados_documentacao(self, caminho_arquivo: str, tipo_arquivo: str) -> str:
            """Faz a extração de informações relevantes da documentação de fonte de dados.
            o parâmetro self não deve ser informado.
            Args:
                caminho_arquivo (str): caminho do arquivo da documentação.
                tipo_arquivo (str): Um dos tipos de arquivo pré definidos (CSV, PDF, TXT).
            """
            
            # Load document
            if tipo_arquivo == 'PDF': raise ToolException(f'A ferramenta não suporta o tipo {tipo_arquivo}')
            with open (caminho_arquivo, 'r') as file:
                  documentation = ''.join(file.readlines())
            chain = self.chain | self.parser
            extract_schema = chain.invoke(
                   {'ordem': f'Você deve extrar as informações necessárias para o engenheiro de dados construir a pipeline de extração da seguinte fonte: {documentation}'})
            

            return extract_schema.model_dump_json()
    
    def __init__(self, model: BaseChatModel, *args, **kargs) -> None:
            super().__init__(*args, **kargs)
            self.tools = [self.extrair_dados_documentacao]
            self.prompt = (ChatPromptTemplate([
                   self.role_prompt,
                   MessagesPlaceholder(variable_name='ordem')])
                   .partial(output_parser=self.parser.get_format_instructions())
                   .partial(tools='.'.join([tool.name for tool in self.tools]))
                   )
            self.agent = model.bind_tools(self.tools)
            self.chain = self.prompt | self.agent
    
    def invoke(self, state: GraphState, **kargs) -> BaseMessage:
        output = self.chain.invoke({'ordem': state['messages']})
        return output

    
    def __call__(self, query: str) -> Any:
           self._response = self.chain.invoke({'ordem': query})
           
           return self._response
    
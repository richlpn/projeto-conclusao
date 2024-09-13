# Imports
#%%
from utils.get_model import MODEL
from agents.extractor import ExtractorSchema, Extractor
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
claude = MODEL(model="claude-3-5-sonnet-20240620", temperature=0)

#%%
meta_data = """Agência Nacional de Telecomunicações – Anatel

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
DescCodEstacaoDebito: descritivo da estação de telecomunicações e suas características distintivas."""

analyser_extract_parser = PydanticOutputParser(pydantic_object=ExtractorSchema)

#%%
analyser_extract_prompt = PromptTemplate(
    template='Aja como especialista em engenharia de pipeline de dados, sua tarefa é {task} os seguintes dados {format_instructions} do conteudo:\n{metadata}',
    input_variables=["metadata"],
    partial_variables={"format_instructions":analyser_extract_parser.get_format_instructions(), "task":"Extrair"}
)

analyser_extract_chain = analyser_extract_prompt | claude | analyser_extract_parser
# %%
extract_schema = analyser_extract_chain.invoke(meta_data)
extractor_agent = Extractor(claude)
extractor_agent.invoke(extract_schema)
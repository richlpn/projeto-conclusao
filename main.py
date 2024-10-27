# from src.graph.graph import GRAPH

# # %%
# DOC = "./static/data/docs/Glossario - Arrecadação - Valores de Tributos e Preços Públicos_v1.txt"


# # %%
# if __name__ == "__main__":
#     msg = [f"Create a new ETL pipeline, from the documentation at {DOC}"]
#     response = GRAPH.invoke({"messages": msg, "origin": "user"})
#     print(response)

from src.models.data_docs_schemas_model import (
    ColumnSchema,
    DataSourceSchema,
    TableSchema,
)
from src.models.agents.task_creation_agent import TASK_CREATION_AGENT

schema = DataSourceSchema(
    name="Arrecadação - Valores de Tributos e Preços Públicos",
    tables=[
        TableSchema(
            type="CSV",
            name="Taxas_Estacoes.csv",
            columns=[
                ColumnSchema(
                    type="str",
                    name="Numservico",
                    description="código numérico identificador do Serviço de Telecomunicação.",
                ),
                ColumnSchema(
                    type="str",
                    name="NomeServico",
                    description="nome do Serviço de Telecomunicação. Serviço de telecomunicação é o conjunto de atividades que possibilita a oferta de telecomunicação.",
                ),
                ColumnSchema(
                    type="str",
                    name="CodReceita",
                    description="código numérico identificador da receita produto da arrecadação das taxas, contribuição e preços públicos.",
                ),
                ColumnSchema(
                    type="str",
                    name="SiglaReceita",
                    description="sigla da receita, sendo: TFI - Taxa de Fiscalização de Instalação; TFI-SAT - Taxa de Fiscalização de Instalação - Satélite; TFF - Taxa de Fiscalização de Funcionamento; TFF-SAT - Taxa de Fiscalização de Funcionamento - Satélite; CFRP - Contribuição para o Fomento da Radiodifusão Pública.",
                ),
                ColumnSchema(
                    type="str",
                    name="codEstacaoDebito",
                    description="código alfabético identificador do tipo de estação de telecomunicações relacionado ao respectivo serviço de telecomunicação.",
                ),
                ColumnSchema(
                    type="str",
                    name="ValorBase",
                    description="valor unitário por estação relativo à receita e ao serviço de telecomunicações.",
                ),
                ColumnSchema(
                    type="str",
                    name="DescCodEstacaoDebito",
                    description="descritivo da estação de telecomunicações e suas características distintivas.",
                ),
            ],
        )
    ],
)

x = TASK_CREATION_AGENT.invoke(SCHEMA=schema)
print(x)

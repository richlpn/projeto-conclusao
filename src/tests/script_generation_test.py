from src.graph.graph import GRAPH
from src.graph.nodes.script_generation_node import generate_python_script
from src.models.requirement_model import Requirement, Task
from src.models.state import ScriptGenerationState

# %%
DOC = "./static/data/docs/Glossario - Arrecadação - Valores de Tributos e Preços Públicos_v1.txt"

state = ScriptGenerationState(
    requirements=Requirement(
        title="",
        tasks=[
            Task(
                title="Read Taxas_Estacoes.csv file",
                description="Use the `TAXAS_ESTACOES_PATH` environment variable to get the path of the CSV file.                      Check if the file exists and raise a FileNotFoundError with message 'File not found at specified path'.                     Use pandas' read_csv function to load the dataframe.",
            ),
            Task(
                title="Validate required columns",
                description="Check if the following columns are present, Raise an Exception with the message 'Missing required columns':                      NumServico, NomeServico, CodReceita, SiglaReceita, codEstacaoDebito, ValorBase, DescCodEstacaoDebito.                     Use pandas' all function to check if all required columns are present.",
            ),
            Task(
                title="Standardize column names",
                description="Write a function 'parse_columns' that takes a string and transforms it into snake_case example:                      NumServico -> num_servico; NomeServico -> nome_servico.                     Apply this function to all column names in the dataframe.",
            ),
            Task(
                title="Convert value types",
                description="Check if the following columns have the correct data type, Raise an Exception with the message 'Incorrect data type':                      NumServico: str -> int; ValorBase: str -> float.                     Use pandas' apply function to convert the data type of each column.",
            ),
            Task(
                title="Load the processed dataframe",
                description="Use the path at `SAILES_OUTPUT_PATH` as parquet file.                      Check if the file already exists and raise a FileExistsError with message 'File already exists'.                     Use pandas' to_parquet function to save the dataframe.",
            ),
        ],
    ),
    completed_tasks=[],
    code=[],
)
# %%
if __name__ == "__main__":
    # msg = [f"Create a new ETL pipeline, from the documentation at {DOC}"]
    # response = GRAPH.invoke({"messages": msg, "origin": "user"})

    print(generate_python_script({"messages": [state]}))

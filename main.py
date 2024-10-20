from src.graph.graph import GRAPH

# %%
DOC = "./static/data/docs/Glossario - Arrecadação - Valores de Tributos e Preços Públicos_v1.txt"


# %%
if __name__ == "__main__":
    msg = [f"Create a new ETL pipeline, from the documentation at {DOC}"]
    response = GRAPH.invoke({"messages": msg, "origin": "user"})
    print(response)

# %%
from fastapi import FastAPI
from src.controller.schema_controller import router
from src.config.database import create_tables

app = FastAPI(debug=True)
app.include_router(router)
create_tables()
# %%
DOC = "static/docs/familias_atendidas_fomento_rural2.txt"


# %%

# msg = [f"Create a new ETL pipeline, from the documentation at {DOC}"]
# response = GRAPH.invoke({"messages": msg, "origin": "user"})
# comp = response["messages"][-1]
# file = comp.save_to_temp_file()
# use sys to run the command "code /tmp/file.py"

# %%

# %%
from fastapi import FastAPI
from src.controller.schema_controller import router

app = FastAPI(debug=True)
app.include_router(router)

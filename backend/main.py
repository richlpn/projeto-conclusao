# %%
from fastapi import FastAPI
from src.controller.schema_controller import router
from src.controller.requirement_controller import router as req_router

app = FastAPI(debug=True)
app.include_router(router)
# app.include_router(req_router)

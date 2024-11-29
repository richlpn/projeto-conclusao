from fastapi import FastAPI
from src.controller.data_source_controller import router as data_source_router
from src.controller.requirement_controller import router as requirement_router

app = FastAPI(debug=True)
app.include_router(data_source_router)
app.include_router(requirement_router)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config import get_settings
from src.controller.data_source_column_controller import (
    router as data_source_column_router,
)
from src.controller.data_source_controller import router as data_source_router
from src.controller.data_source_type_controller import router as data_source_type_router
from src.controller.task_controller import router as task_router
from src.controller.script_generation_controller import router as script_router

settings = get_settings()

app = FastAPI(debug=settings.debug)

origins = [
    "http://localhost:5173",  # frontend service URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data_source_router)
app.include_router(task_router)
app.include_router(data_source_column_router)
app.include_router(data_source_type_router)
app.include_router(script_router)

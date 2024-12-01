from fastapi import FastAPI
from src.config import get_settings
from src.controller.data_source_column_controller import (
    router as data_source_column_router,
)
from src.controller.data_source_controller import router as data_source_router
from src.controller.requirement_controller import router as requirement_router
from src.controller.task_controller import router as task_router

settings = get_settings()
app = FastAPI(debug=settings.debug)
app.include_router(data_source_router)
app.include_router(requirement_router)
app.include_router(task_router)
app.include_router(data_source_column_router)

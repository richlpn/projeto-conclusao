from fastapi import APIRouter
from src.config.app import app


def controller(router: APIRouter):
    app.include_router(router)

    def decorator(cls):
        for route in router.routes:
            if (name := getattr(route, "name")) and hasattr(cls, name):
                setattr(route, "endpoint", getattr(cls(), name))
        return cls

    return decorator

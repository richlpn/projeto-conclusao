from fastapi import APIRouter
from src.config.dependency_injection.component import component


def controller(router: APIRouter):
    def decorator(cls):
        for route in router.routes:
            if (name := getattr(route, "name")) and hasattr(cls, name):
                setattr(route, "endpoint", getattr(cls(), name))
        return cls

    return decorator

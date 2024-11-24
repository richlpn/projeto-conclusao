from typing import Optional, Type
from fastapi import APIRouter
from src.config.dependency_injection.component import component


def controller(router: APIRouter, interface: Optional[Type] = None):
    def decorator(cls):
        for route in router.routes:
            if hasattr(route, "name") and hasattr(cls, route.name):
                route.endpoint = getattr(cls(), route.name)
        return cls

    return decorator

from typing import Type


class DependencyNotFoundError(Exception):
    def __init__(self, dependency_type: Type):
        message = f"Dependency of type `{dependency_type.__class__.__name__}` not found. Please ensure it is registered with the @component decorator."
        super().__init__(message)

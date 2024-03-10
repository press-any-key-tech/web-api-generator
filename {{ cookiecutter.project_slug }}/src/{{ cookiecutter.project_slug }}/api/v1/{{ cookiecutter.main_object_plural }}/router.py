""" Api Routes
"""

from fastapi import APIRouter

from . import api_{{ cookiecutter.main_object_plural }}, api_{{ cookiecutter.main_object_plural }}_{{ cookiecutter.related_object_plural }}

ROUTE_PREFIX: str = "/api/v1/{{ cookiecutter.main_object_plural }}"

api_router = APIRouter()
api_router.include_router(api_{{ cookiecutter.main_object_plural }}.api_router, prefix=ROUTE_PREFIX, tags=["Persons"])
api_router.include_router(
    api_{{ cookiecutter.main_object_plural }}_{{ cookiecutter.related_object_plural }}.api_router, prefix=ROUTE_PREFIX, tags=["PersonsPolicies"]
)

from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from {{ cookiecutter.project_slug }}.domain.entities.{{ cookiecutter.main_object }}_base import {{ cookiecutter.main_object.capitalize() }}Base
from {{ cookiecutter.project_slug }}.domain.entities.{{ cookiecutter.related_object }} import {{ cookiecutter.related_object.capitalize() }}


class {{ cookiecutter.main_object.capitalize() }}({{ cookiecutter.main_object.capitalize() }}Base):
    """
    Represents a data structure when retrieving data.
    """

    {{ cookiecutter.related_object_plural }}: Optional[List[{{ cookiecutter.related_object.capitalize() }}]] = Field(
        default=[],
        json_schema_extra={"description": "{{ cookiecutter.related_object_plural.capitalize() }}"},
    )

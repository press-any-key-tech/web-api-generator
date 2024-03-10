from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from {{ cookiecutter.project_slug }}.domain.entities.{{ cookiecutter.related_object }} import {{ cookiecutter.related_object.capitalize() }}

from {{ cookiecutter.project_slug }}.core.domain.validators import ksuid_validator


class {{ cookiecutter.main_object.capitalize() }}Base(BaseModel):
    """
    Represents a data structure.
    """

    id: Optional[str] = Field(
        default=None,
        json_schema_extra={
            "description": "Unique ID (ksuid)",
            "example": "0ujsswThIGTUYm2K8FjOOfXtY1K",
        },
    )

    name: str = Field(
        ...,
        max_length=500,
        json_schema_extra={
            "description": "Name",
            "example": "John",
        },
    )

    surname: str = Field(
        ...,
        max_length=500,
        json_schema_extra={
            "description": "Surname/s",
            "example": "Doe",
        },
    )

    email: EmailStr = Field(
        ...,
        max_length=150,
        json_schema_extra={
            "description": "Email",
            "example": "johndoe@mail.com",
        },
    )

    {{ cookiecutter.related_object_plural }}: Optional[List[{{ cookiecutter.related_object.capitalize() }}]] = Field(
        default=[],
        json_schema_extra={"description": "{{ cookiecutter.related_object_plural.capitalize() }}"},
    )

    @field_validator("id")
    def validate_ksuid(cls, value, values, **kwargs):
        return ksuid_validator(value)

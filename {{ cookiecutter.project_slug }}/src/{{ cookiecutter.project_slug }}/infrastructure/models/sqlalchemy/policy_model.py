from typing import cast

from ksuid import Ksuid
from sqlalchemy import Column, Enum, ForeignKey, String

from {{ cookiecutter.project_slug }}.core.repository.model.sqlalchemy import Base, BaseModel
from {{ cookiecutter.project_slug }}.domain.types.policy_status_enum import PolicyStatusEnum


class PolicyModel(Base, BaseModel):
    """Repository policies model

    Args:
        Base (_type_): SQLAlchemy base model
        BaseModel (_type_): base entity model
    """

    __tablename__ = "policies"

    id = Column(
        String(27),
        primary_key=True,
        default=lambda: str(Ksuid()),
        index=True,
    )

    person_id = Column(String, ForeignKey("persons.id"), nullable=False)

    policy_number = Column(String(500), nullable=False)
    status = Column(
        Enum(PolicyStatusEnum), nullable=False, default=PolicyStatusEnum.INACTIVE
    )

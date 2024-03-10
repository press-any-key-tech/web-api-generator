"""Dependency injection definition
"""

from pythondi import Provider

from {{ cookiecutter.project_slug }}.core.logging import logger
from {{ cookiecutter.project_slug }}.domain.repository import (
    HealthcheckRepository,
    PersonRepository,
    PolicyRepository,
)
from {{ cookiecutter.project_slug }}.infrastructure.repositories.sqlalchemy.healthcheck_repository_impl import (
    HealthcheckRepositoryImpl,
)
from {{ cookiecutter.project_slug }}.infrastructure.repositories.sqlalchemy.person_repository_impl import (
    PersonRepositoryImpl,
)
from {{ cookiecutter.project_slug }}.infrastructure.repositories.sqlalchemy.policy_repository_impl import (
    PolicyRepositoryImpl,
)


def include_di(provider: Provider):
    """Initialize dependency injection for repositories

    Args:
        provider (Provider): _description_
    """

    logger.debug("Initializing dependency injection")

    # Include your modules
    provider.bind(HealthcheckRepository, HealthcheckRepositoryImpl)
    provider.bind(PersonRepository, PersonRepositoryImpl)
    provider.bind(PolicyRepository, PolicyRepositoryImpl)

from typing import Any, Dict, List
from unittest.mock import AsyncMock, MagicMock, create_autospec, patch

import httpx
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from ksuid import Ksuid
from pythondi import Provider, configure

from {{ cookiecutter.project_slug }}.api.v1.persons.api_persons import api_router, get_list
from {{ cookiecutter.project_slug }}.core.repository.exceptions import ItemNotFoundException
from {{ cookiecutter.project_slug }}.di import include_di
from {{ cookiecutter.project_slug }}.domain.entities import Person, PersonFilter
from {{ cookiecutter.project_slug }}.domain.exceptions import PersonNotFoundException

# To patch the method that makes the API call to repository
PATCH_READ_SERVICE: str = "{{ cookiecutter.project_slug }}.api.v1.persons.api.ReadService"
PATCH_WRITE_SERVICE: str = "{{ cookiecutter.project_slug }}.api.v1.persons.api.WriteService"

# Test client configuration
# Dependency injection (general)
provider: Provider = Provider()
include_di(provider=provider)
configure(provider=provider)

app: FastAPI = FastAPI()
app.include_router(api_router)
client: TestClient = TestClient(app)


@pytest.fixture(autouse=True)
def disable_db_initialization():
    with patch("{{ cookiecutter.project_slug }}.core.settings.settings.INITIALIZE_DATABASE", False):
        yield


@patch("{{ cookiecutter.project_slug }}.core.auth.cognito.settings.settings.AUTH_DISABLED", True)
@pytest.mark.asyncio
async def test_get_list_success():
    # Arrange
    filter: PersonFilter = PersonFilter(name="Person1", surname="Surname1")
    expected_result = [
        Person(
            id=str(Ksuid()), name="Person1", surname="Surname1", email="email1@mail.com"
        ),
        Person(
            id=str(Ksuid()), name="Person2", surname="Surname2", email="email2@mail.com"
        ),
        Person(
            id=str(Ksuid()), name="Person3", surname="Surname3", email="email3@mail.com"
        ),
    ]

    with patch(PATCH_READ_SERVICE) as service_mock:

        async def async_mock():
            return expected_result

        service_mock.return_value.get_list.return_value = async_mock()

        # Act
        response: httpx.Response = client.get("/")  # , params=filter.model_dump())

        # service_mock.return_value.get_list.assert_called_once_with(filter=filter)
        service_mock.return_value.get_list.assert_called_once()

    # Assert

    assert response.status_code == 200

    data: Any = response.json()
    assert isinstance(data, list)

    persons: List[Person] = [Person.model_validate(item) for item in data]
    assert len(persons) == len(expected_result)
    assert persons == expected_result


@patch("{{ cookiecutter.project_slug }}.core.auth.cognito.settings.settings.AUTH_DISABLED", True)
@pytest.mark.asyncio
async def test_get_list_error():

    # Arrange
    # filter: PersonFilter = PersonFilter(name="Person1", surname="Surname1")

    expected_error: Dict[str, str] = {
        "message": "Something went wrong: Simulated error"
    }

    with patch(PATCH_READ_SERVICE) as service_mock:

        service_mock.return_value.get_list = MagicMock(
            side_effect=Exception("Simulated error")
        )

        # Act
        response: httpx.Response = client.get("/")  # , params=filter.model_dump())

    # Assert
    assert response.status_code == 500
    assert response.json() == expected_error


@patch("{{ cookiecutter.project_slug }}.core.auth.cognito.settings.settings.AUTH_DISABLED", True)
@pytest.mark.asyncio
async def test_get_by_id_success():
    # Arrange
    id: str = str(Ksuid())

    expected_result = Person(
        id=id, name="Person1", surname="Surname1", email="email1@mail.com"
    )

    with patch(PATCH_READ_SERVICE) as service_mock:

        async def async_mock():
            return expected_result

        service_mock.return_value.get_by_id.return_value = async_mock()

        # Act
        response: httpx.Response = client.get(f"/{id}")

        # service_mock.return_value.get_list.assert_called_once_with(filter=filter)
        service_mock.return_value.get_by_id.assert_called_once()

    # Assert

    assert response.status_code == 200

    data: Any = response.json()

    person: Person = Person.model_validate(data)
    assert person == expected_result


@patch("{{ cookiecutter.project_slug }}.core.auth.cognito.settings.settings.AUTH_DISABLED", True)
@pytest.mark.asyncio
async def test_get_by_id_error_not_found():

    id: str = str(Ksuid())

    expected_error: Dict[str, str] = {"message": f"Person with id [{id}] not found"}

    with patch(PATCH_READ_SERVICE) as service_mock:

        service_mock.return_value.get_by_id = MagicMock(
            side_effect=PersonNotFoundException(f"Person with id [{id}] not found")
        )

        # Act
        response: httpx.Response = client.get(f"/{id}")

    # Assert
    assert response.status_code == 404
    assert response.json() == expected_error


@patch("{{ cookiecutter.project_slug }}.core.auth.cognito.settings.settings.AUTH_DISABLED", True)
@pytest.mark.asyncio
async def test_create_success():
    # Arrange
    id: str = str(Ksuid())

    expected_result = Person(
        id=id, name="Person1", surname="Surname1", email="email1@mail.com"
    )

    body: Dict[str, str] = {
        "id": id,
        "name": "Person1",
        "surname": "Surname1",
        "email": "email1@mail.com",
    }

    with patch(PATCH_WRITE_SERVICE) as service_mock:

        async def async_mock():
            return expected_result

        service_mock.return_value.create.return_value = async_mock()

        # Act
        response: httpx.Response = client.post("/", json=body)

        # service_mock.return_value.get_list.assert_called_once_with(filter=filter)
        service_mock.return_value.create.assert_called_once()

    # Assert

    assert response.status_code == 201

    data: Any = response.json()

    person: Person = Person.model_validate(data)
    assert person == expected_result


@patch("{{ cookiecutter.project_slug }}.core.auth.cognito.settings.settings.AUTH_DISABLED", True)
@pytest.mark.asyncio
async def test_delete_by_id_success():
    # Arrange
    id: str = str(Ksuid())

    with patch(PATCH_WRITE_SERVICE) as service_mock:

        async def async_mock():
            return None

        service_mock.return_value.delete_by_id.return_value = async_mock()

        # Act
        response: httpx.Response = client.delete(f"/{id}")

        # service_mock.return_value.get_list.assert_called_once_with(filter=filter)
        service_mock.return_value.delete_by_id.assert_called_once()

    # Assert

    assert response.status_code == 204


@patch("{{ cookiecutter.project_slug }}.core.auth.cognito.settings.settings.AUTH_DISABLED", True)
@pytest.mark.asyncio
async def test_delete_by_id_error_not_found():

    id: str = str(Ksuid())

    expected_error: Dict[str, str] = {"message": f"Person with id [{id}] not found"}

    with patch(PATCH_WRITE_SERVICE) as service_mock:

        service_mock.return_value.delete_by_id = MagicMock(
            side_effect=PersonNotFoundException(f"Person with id [{id}] not found")
        )

        # Act
        response: httpx.Response = client.delete(f"/{id}")

    # Assert
    assert response.status_code == 404
    assert response.json() == expected_error


@patch("{{ cookiecutter.project_slug }}.core.auth.cognito.settings.settings.AUTH_DISABLED", True)
@pytest.mark.asyncio
async def test_update_success():
    # Arrange
    id: str = str(Ksuid())

    expected_result = Person(
        id=id, name="Person1", surname="Surname1", email="email1@mail.com"
    )

    body: Dict[str, str] = {
        "id": id,
        "name": "Person1",
        "surname": "Surname1",
        "email": "email1@mail.com",
    }

    with patch(PATCH_WRITE_SERVICE) as service_mock:

        async def async_mock():
            return expected_result

        service_mock.return_value.update.return_value = async_mock()

        # Act
        response: httpx.Response = client.put(f"/{id}", json=body)

        # service_mock.return_value.get_list.assert_called_once_with(filter=filter)
        service_mock.return_value.update.assert_called_once()

    # Assert

    assert response.status_code == 200

    data: Any = response.json()

    person: Person = Person.model_validate(data)
    assert person == expected_result


@patch("{{ cookiecutter.project_slug }}.core.auth.cognito.settings.settings.AUTH_DISABLED", True)
@pytest.mark.asyncio
async def test_update_error_not_found():
    # Arrange
    id: str = str(Ksuid())

    body: Dict[str, str] = {
        "id": id,
        "name": "Person1",
        "surname": "Surname1",
        "email": "email1@mail.com",
    }

    expected_error: Dict[str, str] = {"message": f"Person with id [{id}] not found"}

    with patch(PATCH_WRITE_SERVICE) as service_mock:

        service_mock.return_value.update = MagicMock(
            side_effect=PersonNotFoundException(f"Person with id [{id}] not found")
        )

        # Act
        response: httpx.Response = client.put(f"/{id}", json=body)

    # Assert
    assert response.status_code == 404
    assert response.json() == expected_error

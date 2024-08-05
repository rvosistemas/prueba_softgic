import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.tests.utils.plan import create_random_plan


def test_create_plan(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"nombre": "Plan A", "descripcion": "Plan A description", "activo": True}
    response = client.post(
        f"{settings.API_V1_STR}/plans/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["nombre"] == data["nombre"]
    assert content["descripcion"] == data["descripcion"]
    assert content["activo"] == data["activo"]
    assert "id" in content


def test_read_plan(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    plan = create_random_plan(db)
    response = client.get(
        f"{settings.API_V1_STR}/plans/{plan.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["nombre"] == plan.nombre
    assert content["descripcion"] == plan.descripcion
    assert content["id"] == str(plan.id)
    assert content["activo"] == plan.activo


def test_read_plan_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/plans/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Plan not found"


def test_update_plan(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    plan = create_random_plan(db)
    data = {
        "nombre": "Updated Plan",
        "descripcion": "Updated description",
        "activo": False,
    }
    response = client.put(
        f"{settings.API_V1_STR}/plans/{plan.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["nombre"] == data["nombre"]
    assert content["descripcion"] == data["descripcion"]
    assert content["activo"] == data["activo"]
    assert content["id"] == str(plan.id)


def test_update_plan_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {
        "nombre": "Updated Plan",
        "descripcion": "Updated description",
        "activo": False,
    }
    response = client.put(
        f"{settings.API_V1_STR}/plans/{uuid.uuid4()}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Plan not found"


def test_delete_plan(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    plan = create_random_plan(db)
    response = client.delete(
        f"{settings.API_V1_STR}/plans/{plan.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Plan deleted successfully"


def test_delete_plan_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/plans/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Plan not found"


"""Automated tests for the HR Management System API."""

import pytest
from fastapi.testclient import TestClient

from app.main import app, employees

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_employees():
    """Isolate tests by clearing employee records before each test."""
    employees.clear()
    yield
    employees.clear()


def employee_payload(**overrides):
    """Build a valid employee payload with optional overrides."""
    payload = {
        "name": "Asha Rao",
        "email": "asha@example.com",
        "department": "Engineering",
        "salary": 65000,
    }
    payload.update(overrides)
    return payload


def test_health_check():
    """Verify that the health endpoint returns an OK status."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_list_employee():
    """Verify employee creation and listing."""
    create_response = client.post("/employees", json=employee_payload())
    assert create_response.status_code == 201
    assert create_response.json()["id"] == 1

    list_response = client.get("/employees")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1


def test_get_employee_not_found():
    """Verify that an unknown employee ID returns 404."""
    response = client.get("/employees/999")
    assert response.status_code == 404


def test_reject_invalid_salary():
    """Verify that a non-positive salary is rejected."""
    response = client.post(
        "/employees",
        json=employee_payload(salary=0),
    )
    assert response.status_code == 422


def test_duplicate_email_is_rejected():
    """Verify that duplicate employee email addresses are rejected."""
    client.post("/employees", json=employee_payload())
    response = client.post(
        "/employees",
        json=employee_payload(name="Ravi Kumar"),
    )
    assert response.status_code == 409


def test_update_employee():
    """Verify that an existing employee can be updated."""
    created = client.post("/employees", json=employee_payload()).json()
    response = client.put(
        f"/employees/{created['id']}",
        json=employee_payload(name="Asha Sharma"),
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Asha Sharma"


def test_delete_employee():
    """Verify that an employee can be deleted."""
    created = client.post("/employees", json=employee_payload()).json()
    response = client.delete(f"/employees/{created['id']}")
    assert response.status_code == 204
    assert client.get(f"/employees/{created['id']}").status_code == 404

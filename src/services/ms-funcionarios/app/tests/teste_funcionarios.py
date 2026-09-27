import os
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

os.environ["DATABASE_URL"] = "sqlite://"

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


from ..db.dependeces import get_db
from ..db import querys_funcionario
from ..routes import routes_funcionario

EMPLOYEE = {
    "id": 1,
    "nome": "Ana Silva",
    "cpf": "52998224725",
    "email": "ana@example.com",
    "telefone": "11999999999",
    "data_nascimento": "1990-01-01",
    "cargo": "Caixa",
    "salario": 2000.0,
    "senha": "hashed-password",
    "data_contratacao": "2020-01-01",
    "created_at": None,
    "updated_at": None,
}

@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(routes_funcionario.router, prefix="/api/v1")

    app.dependency_overrides[get_db] = lambda: None

    with TestClient(app) as test_client:
        yield test_client


def test_login_funcionario(client, monkeypatch):
    monkeypatch.setattr(
        routes_funcionario.security,
        "authenticate_user",
        lambda **kwargs: type("User", (), {"cpf": EMPLOYEE["cpf"]})(),
    )
    monkeypatch.setattr(
        routes_funcionario.security,
        "create_access_token",
        lambda data_payload: "test-token",
    )

    response = client.post(
        "/api/v1/funcionarios/auth/",
        params={"cpf": EMPLOYEE["cpf"], "senha": "password"},
    )

    assert response.status_code == 200
    assert response.json() == {"access_token": "test-token", "token_type": "bearer"}


def test_listar_funcionarios(client, monkeypatch):
    monkeypatch.setattr(
        routes_funcionario.querys_funcionario,
        "listar_todos_funcionarios",
        lambda db: [EMPLOYEE],
    )

    response = client.get("/api/v1/funcionarios/")

    assert response.status_code == 200
    assert response.json()[0]["id"] == EMPLOYEE["id"]


def test_listar_todos_funcionarios_nao_aplica_filter_invalido():
    db = MagicMock()
    db.query.return_value.all.return_value = [EMPLOYEE]

    funcionarios = querys_funcionario.listar_todos_funcionarios(db)

    db.query.assert_called_once_with(querys_funcionario.Funcionarios)
    db.query.return_value.filter.assert_not_called()
    assert funcionarios == [EMPLOYEE]


def test_obter_funcionario_por_id(client, monkeypatch):
    monkeypatch.setattr(
        routes_funcionario.querys_funcionario,
        "obter_funcionario",
        lambda db, funcionario_id: EMPLOYEE,
    )

    response = client.get("/api/v1/funcionarios/1")

    assert response.status_code == 200
    assert response.json()["email"] == EMPLOYEE["email"]


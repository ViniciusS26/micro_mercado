import os
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

os.environ["DATABASE_URL"] = "sqlite://"

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from ..db.dependeces import get_db
from ..routes import  routes_produtos

PRODUCT = {
    "id": 2,
    "titulo": "Arroz",
    "descricao": "Arroz tipo 1",
    "preco": 12.5,
    "peso": 5.0,
    "data_fabricacao": "2025-01-01",
    "data_validade": "2026-01-01",
    "data_cadastro": None,
    "data_atualizacao": None,
}


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(routes_produtos.router, prefix="/api/v1")

    app.dependency_overrides[get_db] = lambda: None

    with TestClient(app) as test_client:
        yield test_client



def test_cadastrar_produto(client, monkeypatch):
    monkeypatch.setattr(routes_produtos, "criar_produto", lambda db, produto: PRODUCT)

    response = client.post(
        "/api/v1/produtos/",
        json={
            "titulo": "Arroz",
            "descricao": "Arroz tipo 1",
            "preco": 12.5,
            "peso": 5,
            "data_fabricacao": "2025-01-01",
            "data_validade": "2026-01-01",
        },
    )

    assert response.status_code == 200
    assert response.json()["titulo"] == "Arroz"


def test_obter_produto_por_titulo(client, monkeypatch):
    monkeypatch.setattr(routes_produtos, "obter_produto_por_titulo", lambda db, titulo: PRODUCT)

    response = client.get("/api/v1/produtos/Arroz")

    assert response.status_code == 200
    assert response.json()["id"] == PRODUCT["id"]


def test_listar_produtos(client, monkeypatch):
    monkeypatch.setattr(routes_produtos, "obter_produtos", lambda db: [PRODUCT])

    response = client.get("/api/v1/produtos/")

    assert response.status_code == 200
    assert response.json()[0]["titulo"] == PRODUCT["titulo"]


def test_atualizar_produto(client, monkeypatch):
    monkeypatch.setattr(routes_produtos, "atualiza_produto", lambda db, id, produto: PRODUCT)

    response = client.put("/api/v1/produtos/2", json={"preco": 13})

    assert response.status_code == 200
    assert response.json()["id"] == PRODUCT["id"]


def test_deletar_produto(client, monkeypatch):
    monkeypatch.setattr(routes_produtos, "deleta_produto", lambda db, produto_id: PRODUCT)

    response = client.delete("/api/v1/produtos/2")

    assert response.status_code == 200
    assert response.json()["id"] == PRODUCT["id"]


def test_contar_produtos(client, monkeypatch):
    monkeypatch.setattr(routes_produtos, "contar_produtos", lambda db: 4)

    response = client.get("/api/v1/produtos/contar/")

    assert response.status_code == 200
    assert response.json() == 4


def test_total_valor_produtos(client, monkeypatch):
    monkeypatch.setattr(routes_produtos, "sum_valor_total", lambda db: 57.5)

    response = client.get("/api/v1/produtos/total_valor/")

    assert response.status_code == 200
    assert response.json() == 57.5


def test_obter_produto_por_id(client, monkeypatch):
    monkeypatch.setattr(routes_produtos, "obter_produto_id", lambda db, id: PRODUCT)

    response = client.get("/api/v1/produtos/id/2")

    assert response.status_code == 200
    assert response.json()["titulo"] == PRODUCT["titulo"]
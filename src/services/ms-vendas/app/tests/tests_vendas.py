import os
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

os.environ["DATABASE_URL"] = "sqlite://"

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from ..db.dependeces import get_db
from ..db import querys_vendas
from ..routes import routes_vendas


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



SALE = {
    "id": 3,
    "funcionario_id": 1,
    "nome_funcionario": "Ana Silva",
    "cpf": "52998224725",
    "cargo": "Caixa",
    "data_venda": datetime(2025, 1, 1).isoformat(),
    "valor_total": 12.5,
    "itens": [],
}


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(routes_vendas.router, prefix="/api/v1")
    app.dependency_overrides[get_db] = lambda: None

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()
    with TestClient(app) as test_client:
        yield test_client


def test_criar_venda(client, monkeypatch):
    async def buscar_produto(titulo):
        return {"id": PRODUCT["id"], "titulo": PRODUCT["titulo"], "preco": PRODUCT["preco"]}

    async def buscar_funcionario(funcionario_id):
        return {
            "id": EMPLOYEE["id"],
            "nome": EMPLOYEE["nome"],
            "cpf": EMPLOYEE["cpf"],
            "cargo": EMPLOYEE["cargo"],
        }

    monkeypatch.setattr(routes_vendas, "buscar_produtos_service", buscar_produto)
    monkeypatch.setattr(routes_vendas, "buscar_funcionario_service", buscar_funcionario)
    monkeypatch.setattr(routes_vendas, "criar_venda", lambda db, venda: SALE)

    response = client.post(
        "/api/v1/vendas/",
        json={"titulo_produto": "Arroz", "id_funcionario": 1},
    )

    assert response.status_code == 200
    assert response.json()["funcionario_id"] == EMPLOYEE["id"]


def test_listar_vendas(client, monkeypatch):
    page = {
        "estatisticas": {
            "total_registros": 1,
            "valor_total_periodo": 12.5,
            "total_produtos_periodo": 1,
        },
        "vendas": [SALE],
    }
    monkeypatch.setattr(routes_vendas, "listar_vendas", lambda **kwargs: page)

    response = client.get("/api/v1/vendas/")

    assert response.status_code == 200
    assert response.json()["estatisticas"]["total_registros"] == 1


def test_obter_venda_por_id(client, monkeypatch):
    monkeypatch.setattr(routes_vendas, "obter_venda_por_id", lambda db, venda_id: SALE)

    response = client.get("/api/v1/vendas/3")

    assert response.status_code == 200
    assert response.json()["id"] == SALE["id"]


def test_relatorio_de_vendas_por_funcionario(client, monkeypatch):
    report = {
        "estatisticas": {
            "total_vendas": 1,
            "valor_total_vendido": 12.5,
            "total_produtos_vendidos": 1,
        },
        "vendas": [SALE],
    }
    monkeypatch.setattr(
        routes_vendas,
        "obter_relatorio_por_funcionario",
        lambda **kwargs: report,
    )

    response = client.get("/api/v1/vendas/funcionario/1")

    assert response.status_code == 200
    assert response.json()["estatisticas"]["total_vendas"] == 1


def test_deletar_venda(client, monkeypatch):
    monkeypatch.setattr(routes_vendas, "deletar_venda", lambda db, venda_id: SALE)

    response = client.delete("/api/v1/vendas/3")

    assert response.status_code == 200
    assert response.json()["id"] == SALE["id"]


def test_atualizar_venda(client, monkeypatch):
    monkeypatch.setattr(routes_vendas, "atualizar_venda", lambda db, venda_id, venda_update: SALE)

    response = client.put(
        "/api/v1/vendas/3",
        json={
            "funcionario_id": 1,
            "nome_funcionario": "Ana Silva",
            "cpf": "52998224725",
            "cargo": "Caixa",
            "itens": [{"produto_id": 2, "quantidade": 1, "preco_unitario": 12.5}],
        },
    )

    assert response.status_code == 200
    assert response.json()["id"] == SALE["id"]


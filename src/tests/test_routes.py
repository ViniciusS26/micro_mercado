import os
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

os.environ["DATABASE_URL"] = "sqlite://"

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from db.dependeces import get_db
from db import querys_funcionario
from routes import routes_funcionario, routes_produtos, routes_relatorio, routes_vendas


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
    app.include_router(routes_funcionario.router, prefix="/api/v1")
    app.include_router(routes_produtos.router, prefix="/api/v1")
    app.include_router(routes_vendas.router, prefix="/api/v1")
    app.include_router(routes_relatorio.router, prefix="/api/v1")
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


def test_criar_funcionario_sem_endereco(client, monkeypatch):
    monkeypatch.setattr(
        routes_funcionario.querys_funcionario,
        "obter_funcionarios_email",
        lambda db, email: None,
    )
    monkeypatch.setattr(
        routes_funcionario.querys_funcionario,
        "obter_funcionarios_cpf",
        lambda db, cpf: None,
    )
    monkeypatch.setattr(
        routes_funcionario.querys_funcionario,
        "criar_funcionario",
        lambda db, funcionario: EMPLOYEE,
    )

    response = client.post(
        "/api/v1/funcionarios/",
        json={
            "nome": "Ana Silva",
            "cpf": "52998224725",
            "email": "ana@example.com",
            "telefone": "11999999999",
            "data_nascimento": "1990-01-01",
            "cargo": "Caixa",
            "salario": 2000,
            "senha": "password123",
            "data_contratacao": "2020-01-01",
        },
    )

    assert response.status_code == 200
    assert response.json()["id"] == EMPLOYEE["id"]


def test_atualizar_funcionario(client, monkeypatch):
    monkeypatch.setattr(
        routes_funcionario.querys_funcionario,
        "atualizar_funcionario",
        lambda db, funcionario_id, funcionario: EMPLOYEE,
    )

    response = client.put("/api/v1/funcionarios/1", json={"telefone": "11888888888"})

    assert response.status_code == 200
    assert response.json()["id"] == EMPLOYEE["id"]


def test_deletar_funcionario(client, monkeypatch):
    monkeypatch.setattr(
        routes_funcionario.querys_funcionario,
        "deletar_funcionario",
        lambda db, funcionario_id: EMPLOYEE,
    )

    response = client.delete("/api/v1/funcionarios/1")

    assert response.status_code == 200
    assert response.json() == {"detail": "Funcionário deletado"}


def test_atualizar_endereco(client, monkeypatch):
    address = {
        "funcionario_id": 1,
        "logradouro": "Rua A",
        "numero": "10",
        "complemento": None,
        "bairro": "Centro",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01000-000",
    }
    monkeypatch.setattr(
        routes_funcionario.querys_funcionario,
        "atualizar_endereco",
        lambda db, endereco_id, endereco: address,
    )

    response = client.put("/api/v1/funcionarios/endereco/1", json={"logradouro": "Rua A"})

    assert response.status_code == 200
    assert response.json()["funcionario_id"] == 1


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


def test_obter_produto_da_venda_por_titulo(client, monkeypatch):
    async def buscar_produto(titulo):
        return {"id": PRODUCT["id"], "titulo": PRODUCT["titulo"], "preco": PRODUCT["preco"]}

    monkeypatch.setattr(routes_vendas, "buscar_produtos_service", buscar_produto)

    response = client.get("/api/v1/vendas/produtos/Arroz")

    assert response.status_code == 200
    assert response.json()["id"] == PRODUCT["id"]


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


def test_relatorio_sumario_vendas(client, monkeypatch):
    monkeypatch.setattr(
        routes_relatorio,
        "obter_sumario_vendas_periodo",
        AsyncMock(
            return_value={
                "total_vendas": 1,
                "valor_total_vendido": 12.5,
                "total_produtos_vendidos": 1,
            }
        ),
    )

    response = client.get("/api/v1/relatorios/vendas-sumario")

    assert response.status_code == 200
    assert response.json()["total_vendas"] == 1


def test_relatorio_vendas_por_periodo(client, monkeypatch):
    monkeypatch.setattr(
        routes_relatorio,
        "obter_vendas_por_periodo",
        AsyncMock(return_value={"granularidade": "dia", "series": []}),
    )

    response = client.get("/api/v1/relatorios/vendas-por-periodo")

    assert response.status_code == 200
    assert response.json() == {"granularidade": "dia", "series": []}


def test_ranking_produtos(client, monkeypatch):
    monkeypatch.setattr(
        routes_relatorio,
        "obter_ranking_produtos",
        AsyncMock(return_value={"ordenar_por": "valor", "top": 10, "itens": []}),
    )

    response = client.get("/api/v1/relatorios/ranking-produtos")

    assert response.status_code == 200
    assert response.json()["ordenar_por"] == "valor"


def test_ranking_funcionarios(client, monkeypatch):
    monkeypatch.setattr(
        routes_relatorio,
        "obter_ranking_funcionarios",
        AsyncMock(return_value={"ordenar_por": "valor", "top": 10, "itens": []}),
    )

    response = client.get("/api/v1/relatorios/ranking-funcionarios")

    assert response.status_code == 200
    assert response.json()["ordenar_por"] == "valor"
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.connection import get_db
from app.db.database import Base

# --- Configuração do Ambiente de Teste ---
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost:5432/db_vendas_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """
    Cria um banco de dados limpo para cada função de teste e fornece uma sessão.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def test_client(db_session):
    """
    Cria um cliente de API que usa a sessão de teste.
    """
    def override_get_db_for_test():
        try:
            yield db_session
        finally:
            pass # A fixture db_session já cuida de fechar a conexão

    app.dependency_overrides[get_db] = override_get_db_for_test
    yield TestClient(app)
    app.dependency_overrides.clear()


# --- Testes ---

def test_criar_venda_sucesso(test_client):
    """
    Testa a criação de uma venda com dados válidos.
    """
    payload = {
      "funcionario_id": 1,
      "itens": [{"produto_id": 101, "quantidade": 2, "preco_unitario": 10.00}]
    }
    response = test_client.post("/api/v1/vendas/", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["funcionario_id"] == 1
    assert data["valor_total"] == 20.00
    assert len(data["itens"]) == 1

def test_obter_venda_por_id_sucesso(test_client):
    """
    Testa a busca de uma venda que existe.
    """
    payload = {"funcionario_id": 2, "itens": [{"produto_id": 202, "quantidade": 1, "preco_unitario": 50.0}]}
    response_create = test_client.post("/api/v1/vendas/", json=payload)
    venda_id = response_create.json()["id"]

    response_get = test_client.get(f"/api/v1/vendas/{venda_id}")

    assert response_get.status_code == 200
    data = response_get.json()
    assert data["id"] == venda_id

def test_obter_venda_nao_encontrada(test_client):
    """
    Testa a busca por uma venda com um ID que não existe.
    """
    response = test_client.get("/api/v1/vendas/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Venda não encontrada"

def test_deletar_venda_sucesso(test_client):
    """
    Testa a exclusão de uma venda.
    """
    payload = {"funcionario_id": 3, "itens": [{"produto_id": 303, "quantidade": 3, "preco_unitario": 5.0}]}
    response_create = test_client.post("/api/v1/vendas/", json=payload)
    venda_id = response_create.json()["id"]

    response_delete = test_client.delete(f"/api/v1/vendas/{venda_id}")

    assert response_delete.status_code == 200
    assert response_delete.json()["id"] == venda_id

    response_get = test_client.get(f"/api/v1/vendas/{venda_id}")
    assert response_get.status_code == 404
    
def test_atualizar_venda_sucesso(test_client):
    """
    Testa a atualização bem-sucedida de uma venda.
    """
    payload_inicial = {
        "funcionario_id": 5,
        "itens": [{"produto_id": 505, "quantidade": 1, "preco_unitario": 100.0}]
    }
    response_create = test_client.post("/api/v1/vendas/", json=payload_inicial)
    assert response_create.status_code == 200
    venda_id = response_create.json()["id"]

    payload_update = {
        "funcionario_id": 6,
        "itens": [
            {"produto_id": 606, "quantidade": 2, "preco_unitario": 25.0},
            {"produto_id": 707, "quantidade": 1, "preco_unitario": 50.0}
        ]
    }

    response_update = test_client.put(f"/api/v1/vendas/{venda_id}", json=payload_update)

    assert response_update.status_code == 200
    data_atualizada = response_update.json()

    assert data_atualizada["id"] == venda_id
    assert data_atualizada["funcionario_id"] == 6
    # Verifica se o valor total foi recalculado corretamente: (2 * 25) + 50 = 100
    assert data_atualizada["valor_total"] == 100.0
    assert len(data_atualizada["itens"]) == 2
    assert data_atualizada["itens"][0]["produto_id"] == 606

def test_atualizar_venda_nao_encontrada(test_client):
    """
    Testa a tentativa de atualizar uma venda que não existe.
    """
    payload_update = {
        "funcionario_id": 9,
        "itens": [{"produto_id": 909, "quantidade": 1, "preco_unitario": 10.0}]
    }
    response = test_client.put("/api/v1/vendas/9999", json=payload_update)
    assert response.status_code == 404
    assert response.json()["detail"] == "Venda não encontrada para atualização"
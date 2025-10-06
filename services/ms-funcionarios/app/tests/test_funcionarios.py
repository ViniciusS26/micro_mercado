from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import pytest


from app.main import app 

from ..db.connection import get_db

from .database_test import TestingSessionLocal, setup_database


def override_get_db():
    database = None
    try:
        setup_database() 
        database = TestingSessionLocal()
        yield database
    finally:
        if database:
            database.close()


app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


def test_criar_funcionario_com_sucesso():
    """
    Testa a criação de um funcionário com dados válidos.
    O resultado esperado é um status code 200 e os dados retornados corretamente.
    """
    # Dados de exemplo que vamos enviar para a API
    payload = {
        "nome": "Funcionário Teste",
        "email": "teste@email.com",
        "cpf": "11122233344",
        "telefone": "88999998888",
        "data_nascimento": "1990-01-01",
        "cargo": "Desenvolvedor",
        "salario": 5000.00,
        "senha": "senhaSegura123",
        "data_contratacao": "2023-01-01",
        "enderecos": {
            "logradouro": "Rua do Teste",
            "numero": "123",
            "bairro": "Bairro Teste",
            "cidade": "Picos",
            "estado": "PI",
            "cep": "64600-000"
        }
    }

    # Faz a requisição POST para a nossa rota
    response = client.post("/funcionarios/", json=payload)

    # Verifica os resultados (Assertions)
    assert response.status_code == 200, response.text
    
    data = response.json()
    assert data["email"] == payload["email"]
    assert "id" in data
    assert data["endereco"]["cidade"] == payload["enderecos"]["cidade"]
    assert data["endereco"]["estado"] == "PI"


def test_criar_funcionario_com_email_duplicado():
    """
    Testa a tentativa de criar um funcionário com um email que já existe.
    O resultado esperado é um status code 400.
    """
    payload = {
        "nome": "Outro Teste",
        "email": "duplicado@email.com",
        "cpf": "55566677788",
        "enderecos": { "logradouro": "Rua", "numero": "1", "bairro": "Bairro", "cidade": "Cidade", "estado": "PI", "cep": "12345-678"}
    }

    # 1. Cria o funcionário pela primeira vez (deve funcionar)
    response1 = client.post("/funcionarios/", json=payload)
    assert response1.status_code == 200

    # 2. Tenta criar o MESMO funcionário de novo
    response2 = client.post("/funcionarios/", json=payload)

    # Verifica os resultados
    assert response2.status_code == 400
    assert response2.json()["detail"] == "Email já cadastrado"
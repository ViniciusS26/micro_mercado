import pytest
from fastapi.testclient import TestClient
from httpx import Response, RequestError, HTTPStatusError # Importações corretas
from datetime import date

from app.main import app
from app.schemas import schemas_relatorios as schemas

client = TestClient(app)

# --- Testes ---

@pytest.mark.asyncio # Marcar como teste assíncrono pode ajudar
async def test_gerar_relatorio_sumario_vendas_sucesso(mocker):
    """
    Testa o cenário de sucesso, simulando uma resposta 200 OK do ms-vendas.
    """
    mock_response_data = {
        "estatisticas": {
            "total_registros": 15, "valor_total_periodo": 1234.50, "total_produtos_periodo": 42
        }, "vendas": []
    }

    # Simula o objeto Response
    mock_response = mocker.Mock(spec=Response)
    mock_response.status_code = 200
    mock_response.json.return_value = mock_response_data
    # Simula o método raise_for_status para não fazer nada em caso de sucesso
    mock_response.raise_for_status.return_value = None 

    # Simula o método get do cliente assíncrono
    mock_async_get = mocker.AsyncMock(return_value=mock_response)

    # Simula o próprio AsyncClient para retornar um contexto que tem o método get mockado
    mock_async_client = mocker.AsyncMock()
    mock_async_client.__aenter__.return_value.get = mock_async_get # Atribui o get mockado ao cliente dentro do contexto

    # Patchea o httpx.AsyncClient para retornar o nosso cliente mockado
    mocker.patch("app.services.vendas_service.httpx.AsyncClient", return_value=mock_async_client)

    # Faz a requisição para o nosso endpoint no ms-relatorios
    response = client.get("/api/v1/relatorios/vendas-sumario?data_inicio=2025-10-01&data_fim=2025-10-22")

    # Verifica os resultados
    assert response.status_code == 200
    mock_async_get.assert_awaited_once() # Verifica se o get assíncrono foi chamado
    data = response.json()
    assert data["periodo_inicio"] == "2025-10-01"
    assert data["total_vendas"] == 15
    assert data["valor_total_vendido"] == 1234.50
    assert data["total_produtos_vendidos"] == 42

def test_gerar_relatorio_sumario_vendas_erro_conexao(mocker):
    # CORREÇÃO: Usar o caminho completo para o patch
    mock_get = mocker.patch(
        "app.services.vendas_service.httpx.AsyncClient.get",
        side_effect=RequestError("Erro de conexão simulado")
    )

    response = client.get("/api/v1/relatorios/vendas-sumario")

    assert response.status_code == 503
    mock_get.assert_called_once() # Verifica se a tentativa de chamada ocorreu
    assert "Erro ao comunicar com o serviço de vendas" in response.json()["detail"]

def test_gerar_relatorio_sumario_vendas_erro_servico_vendas(mocker):
    mock_response = Response(500, text="Erro interno no ms-vendas")
    
    # CORREÇÃO: Usar o caminho completo para os patches
    # Mock para raise_for_status precisa do caminho correto também
    mock_raise = mocker.patch(
        "app.services.vendas_service.httpx.Response.raise_for_status", 
        side_effect=HTTPStatusError("Erro 500 simulado", request=mocker.Mock(), response=mock_response)
    )
    mock_get = mocker.patch(
        "app.services.vendas_service.httpx.AsyncClient.get", 
        return_value=mock_response
    )

    response = client.get("/api/v1/relatorios/vendas-sumario")

    assert response.status_code == 500
    mock_get.assert_called_once() # Verifica a chamada
    # mock_raise.assert_called_once() # Verifica se raise_for_status foi chamado (opcional)
    assert "Serviço de vendas retornou erro: Erro interno no ms-vendas" in response.json()["detail"]
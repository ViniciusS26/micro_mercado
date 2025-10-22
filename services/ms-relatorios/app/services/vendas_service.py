import httpx
from datetime import date
from typing import Optional
from fastapi import HTTPException

from ..schemas import schemas_relatorios as schemas # Importa os nossos schemas de relatório

# URL base da API do ms-vendas (deve ser configurável no futuro)
MS_VENDAS_URL = "http://localhost:8000/api/v1/vendas/" # Assumindo que ms-vendas corre na porta 8000

async def obter_sumario_vendas_periodo(
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None
) -> schemas.RelatorioVendasSumario:
    """
    Busca as estatísticas de vendas do ms-vendas para um determinado período.
    """
    params = {}
    if data_inicio:
        params["data_inicio"] = str(data_inicio)
    if data_fim:
        params["data_fim"] = str(data_fim)
        
    # Pedimos limit=0 para obter apenas as estatísticas, sem a lista de vendas
    params["limit"] = "0"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(MS_VENDAS_URL, params=params)
            response.raise_for_status() # Lança exceção para erros HTTP (4xx ou 5xx)
            
            data = response.json()
            
            # Verifica se a resposta tem a estrutura esperada (com estatísticas)
            if "estatisticas" not in data:
                raise HTTPException(status_code=500, detail="Resposta inválida do serviço de vendas (sem estatísticas)")

            stats = data["estatisticas"]

            # Cria o objeto de relatório com os dados obtidos
            relatorio = schemas.RelatorioVendasSumario(
                periodo_inicio=data_inicio,
                periodo_fim=data_fim,
                total_vendas=stats.get("total_registros", 0), 
                valor_total_vendido=stats.get("valor_total_periodo", 0.0),
                total_produtos_vendidos=stats.get("total_produtos_periodo", 0) 
            )
            return relatorio

        except httpx.RequestError as exc:
            # Erro ao tentar conectar/comunicar com o ms-vendas
            raise HTTPException(status_code=503, detail=f"Erro ao comunicar com o serviço de vendas: {exc}")
        except httpx.HTTPStatusError as exc:
            # ms-vendas retornou um erro (4xx ou 5xx)
            raise HTTPException(status_code=exc.response.status_code, detail=f"Serviço de vendas retornou erro: {exc.response.text}")
        except Exception as exc:
            # Outros erros inesperados (ex: parsing do JSON)
            raise HTTPException(status_code=500, detail=f"Erro inesperado ao processar dados de vendas: {exc}")
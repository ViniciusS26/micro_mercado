from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
from datetime import date
from fastapi import Query
from datetime import date

# Importa o schema de resposta e a função do serviço
from ..schemas import schemas_relatorios as schemas
from ..services import vendas_service

# (Opcional: Importar get_db se precisar de acesso ao banco de dados do ms-relatorios)
# from ..db.connection import get_db
# from sqlalchemy.orm import Session

router = APIRouter(prefix="/relatorios")

@router.get(
    "/vendas-sumario", 
    response_model=schemas.RelatorioVendasSumario
)
async def gerar_relatorio_sumario_vendas(
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None
    # , db: Session = Depends(get_db) # Descomentar se precisar do DB
):
    """
    Gera um relatório sumário de vendas (total, valor, produtos)
    para um período especificado, buscando dados do ms-vendas.
    """
    try:
        # Chama a função assíncrona do nosso serviço para buscar os dados
        relatorio = await vendas_service.obter_sumario_vendas_periodo(
            data_inicio=data_inicio,
            data_fim=data_fim
        )
        return relatorio
    except HTTPException as e:
        # Re-levanta exceções HTTP que podem vir do vendas_service
        raise e
    except Exception as e:
        # Captura outros erros inesperados
        raise HTTPException(status_code=500, detail=f"Erro interno ao gerar relatório: {e}")
    
@router.get(
    "/vendas-por-periodo",
    response_model=schemas.RelatorioVendasPorPeriodo
)
async def vendas_por_periodo(
    data_inicio: date | None = None,
    data_fim: date | None = None,
    granularidade: str = Query("dia", pattern="^(dia|mes)$")
):
    """
    Série temporal de vendas agregadas por dia ou mês.
    """
    try:
        return await vendas_service.obter_vendas_por_periodo(
            data_inicio=data_inicio,
            data_fim=data_fim,
            granularidade=granularidade,
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao gerar relatório por período: {e}")
    



@router.get(
    "/ranking-produtos",
    response_model=schemas.RelatorioRankingProdutos
)
async def ranking_produtos(
    data_inicio: date | None = None,
    data_fim: date | None = None,
    ordenar_por: str = Query("valor", pattern="^(qtd|valor)$"),
    top: int = Query(10, ge=1, le=1000),
    incluir_titulos: bool = Query(False, description="Se true, busca 'titulo' no ms-produtos")
):
    """
    Top-N de produtos por quantidade vendida ou valor faturado.
    """
    try:
        return await vendas_service.obter_ranking_produtos(
            data_inicio=data_inicio,
            data_fim=data_fim,
            ordenar_por=ordenar_por,
            top=top,
            incluir_titulos=incluir_titulos,
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao gerar ranking de produtos: {e}")
    
    

@router.get(
    "/ranking-funcionarios",
    response_model=schemas.RelatorioRankingFuncionarios
)
async def ranking_funcionarios(
    data_inicio: date | None = None,
    data_fim: date | None = None,
    ordenar_por: str = Query("valor", pattern="^(qtd|valor)$"),
    top: int = Query(10, ge=1, le=1000),
    incluir_nomes: bool = Query(False, description="Se true, busca 'nome' no ms-funcionarios")
):
    """
    Top-N de funcionários por quantidade de vendas ou por valor faturado.
    """
    try:
        return await vendas_service.obter_ranking_funcionarios(
            data_inicio=data_inicio,
            data_fim=data_fim,
            ordenar_por=ordenar_por,
            top=top,
            incluir_nomes=incluir_nomes,
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao gerar ranking de funcionários: {e}")
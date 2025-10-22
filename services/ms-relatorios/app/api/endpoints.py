from fastapi import APIRouter, Depends, HTTPException
from typing import Optional
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
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date, datetime

from pydantic import BaseModel, ConfigDict
from typing import List, Literal

class VendasPeriodoItem(BaseModel):
    periodo: str                  # "YYYY-MM-DD" (dia) ou "YYYY-MM" (mês)
    quantidade_vendas: int
    valor_total: float

    model_config = ConfigDict(from_attributes=True)

class RelatorioVendasPorPeriodo(BaseModel):
    granularidade: Literal["dia", "mes"]
    series: List[VendasPeriodoItem]

    model_config = ConfigDict(from_attributes=True)

class RelatorioVendasSumario(BaseModel):
    """
    Define a estrutura do relatório sumário de vendas gerado.
    """
    periodo_inicio: Optional[date] = None
    periodo_fim: Optional[date] = None
    total_vendas: int
    valor_total_vendido: float
    total_produtos_vendidos: int
    # Poderíamos adicionar mais campos aqui no futuro, como:
    # ticket_medio: Optional[float] = None
    # produtos_mais_vendidos: List[dict] = [] 

    model_config = ConfigDict(from_attributes=True) # Permite criar a partir de objetos ORM, se necessário

class RankingProdutoItem(BaseModel):
    produto_id: int
    titulo: str | None = None
    qtd_total: int
    valor_total: float

    model_config = ConfigDict(from_attributes=True)

class RelatorioRankingProdutos(BaseModel):
    ordenar_por: Literal["qtd", "valor"]
    top: int
    itens: List[RankingProdutoItem]

    model_config = ConfigDict(from_attributes=True)
    
    
class RankingFuncionarioItem(BaseModel):
    funcionario_id: int
    nome: str | None = None
    qtd_vendas: int
    valor_total: float

    model_config = ConfigDict(from_attributes=True)

class RelatorioRankingFuncionarios(BaseModel):
    ordenar_por: Literal["qtd", "valor"]
    top: int
    itens: List[RankingFuncionarioItem]

    model_config = ConfigDict(from_attributes=True)
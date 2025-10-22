from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import date, datetime

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

# (Poderíamos adicionar aqui schemas para filtros se fossem mais complexos,
# mas por agora data_inicio e data_fim podem ser recebidos diretamente nos endpoints)
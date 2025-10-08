from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

# --- Schemas para ItemVenda ---

class ItemVendaBase(BaseModel):
    produto_id: int
    quantidade: int
    preco_unitario: float

class ItemVendaCreate(ItemVendaBase):
    pass

class ItemVenda(ItemVendaBase):
    id: int
    venda_id: int

    model_config = ConfigDict(from_attributes=True)

# --- Schemas para Venda ---

class VendaBase(BaseModel):
    funcionario_id: int

class VendaCreate(VendaBase):
    itens: List[ItemVendaCreate]

class Venda(VendaBase):
    id: int
    data_venda: datetime
    valor_total: float
    itens: List[ItemVenda] = []

    model_config = ConfigDict(from_attributes=True)
    
class PaginaVendasStats(BaseModel):
    """Estatísticas agregadas para a consulta de vendas."""
    total_registros: int
    valor_total_periodo: float
    total_produtos_periodo: int

class PaginaVendas(BaseModel):
    """Schema completo para a resposta da listagem de vendas."""
    estatisticas: PaginaVendasStats
    vendas: List[Venda]

    model_config = ConfigDict(from_attributes=True)
    
    
class RelatorioFuncionarioStats(BaseModel):
    """Estatísticas agregadas das vendas do funcionário."""
    total_vendas: int
    valor_total_vendido: float
    total_produtos_vendidos: int

class RelatorioFuncionario(BaseModel):
    """Schema completo para a resposta do relatório."""
    estatisticas: RelatorioFuncionarioStats
    vendas: List[Venda]

    model_config = ConfigDict(from_attributes=True)
    

class VendaUpdate(VendaBase):
    itens: List[ItemVendaCreate]
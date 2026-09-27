from pydantic import BaseModel,field_validator, ConfigDict, Field,model_validator
from typing import Optional
from datetime import date, datetime


class ProdutoBase(BaseModel):
    id: Optional[int] = None
    titulo: str
    descricao: str
    preco: float
    peso: float
    data_fabricacao: date
    data_validade: date
    data_cadastro: Optional[datetime] = None
    data_atualizacao: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class ProdutoResponse(BaseModel):
    titulo: str
    descricao: str
    preco: float
    peso: float
    data_fabricacao: date
    data_validade: date
    data_cadastro: Optional[datetime] = None
    data_atualizacao: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

class ProdutoCreate(BaseModel):
    titulo: str
    descricao: str
    preco: float
    peso: float
    data_fabricacao: date
    data_validade: date

    # ==========================================
    # 1. Validações e Limpezas por Campo
    # ==========================================

    @field_validator('titulo', 'descricao')
    @classmethod
    def remover_espacos_sobrando(cls, value: str) -> str:
        """Remove espaços no início/fim e garante que o campo não contenha apenas espaços."""
        texto_limpo = value.strip()
        if not texto_limpo:
            raise ValueError('O campo não pode conter apenas espaços em branco.')
        return texto_limpo

    @field_validator('data_fabricacao')
    @classmethod
    def validar_data_fabricacao(cls, data_fab: date) -> date:
        """Garante que a data de fabricação não esteja no futuro."""
        if data_fab > date.today():
            raise ValueError('A data de fabricação não pode ser uma data futura.')
        return data_fab

    # ==========================================
    # 2. Validação Cruzada entre Campos (Model Validator)
    # ==========================================

    @model_validator(mode='after')
    def validar_datas_produto(self) -> 'ProdutoCreate':
        """Garante que a data de validade seja posterior à data de fabricação e não esteja vencida."""
        if self.data_validade <= self.data_fabricacao:
            raise ValueError('A data de validade deve ser posterior à data de fabricação.')
        
        if self.data_validade < date.today():
            raise ValueError('Não é possível cadastrar um produto com data de validade já vencida.')

        return self
        

    model_config = ConfigDict(from_attributes=True)

   


class ProdutoUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None 
    preco: Optional[float] = None
    peso: Optional[float] = None

     # ==========================================
    # 1. Validações e Limpezas por Campo
    # ==========================================

    @field_validator('titulo', 'descricao')
    @classmethod
    def remover_espacos_sobrando(cls, value: str) -> str:
        """Remove espaços no início/fim e garante que o campo não contenha apenas espaços."""
        texto_limpo = value.strip()
        if not texto_limpo:
            raise ValueError('O campo não pode conter apenas espaços em branco.')
        return texto_limpo


    model_config = ConfigDict(from_attributes=True)

class Produto(ProdutoBase):
    id: int


    model_config = ConfigDict(from_attributes=True)
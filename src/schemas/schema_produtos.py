from pydantic import BaseModel,field_validator, ConfigDict
from typing import List, Optional
from datetime import date, datetime
from validate_docbr import CPF

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

class ProdutoCreate(BaseModel):
    titulo: str
    descricao: str
    preco: float
    peso: float
    data_fabricacao: date
    data_validade: date

    model_config = ConfigDict(from_attributes=True)

   


class ProdutoUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None 
    preco: Optional[float] = None
    peso: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)

class Produto(ProdutoBase):
    id: int


    model_config = ConfigDict(from_attributes=True)
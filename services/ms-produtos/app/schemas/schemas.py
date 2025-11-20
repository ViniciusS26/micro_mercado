from pydantic import BaseModel, EmailStr, field_validator
from typing import List, Optional
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

class ProdutoCreate(BaseModel):
    titulo: str
    descricao: str
    preco: float
    peso: float
    data_fabricacao: date
    data_validade: date

   


class ProdutoUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None 
    preco: Optional[float] = None
    peso: Optional[float] = None

class Produto(ProdutoBase):
    id: int

    class Config:
        orm_mode = True

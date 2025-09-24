from pydantic import BaseModel,field_validator, ConfigDict
from typing import List
from datetime import date, datetime







class FuncionarioResponse(BaseModel):
    id: int
    nome: str
    cpf: str
    email: str
    telefone: str
    cargo: str
    data_contratacao: date
    data_cadastro: datetime = datetime.now()
    model_config = ConfigDict(from_attributes=True)

class FuncionarioCreate(BaseModel):
    nome: str
    cpf: str
    email: str
    telefone: str
    cargo: str
    data_contratacao: date


    
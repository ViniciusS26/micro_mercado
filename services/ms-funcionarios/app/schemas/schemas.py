from pydantic import BaseModel,field_validator, ConfigDict
from typing import List
from datetime import date, datetime





class FuncionarioResponse(BaseModel):
    id: int
    nome: str
    cpf: str
    email: str
    telefone: str
    data_nascimento: date
    cargo: str
    salario: float
    senha: str
    data_contratacao: date
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

class FuncionarioCreate(BaseModel):
    nome: str
    cpf: str
    email: str
    telefone: str
    data_nascimento: date
    cargo: str
    salario: float
    senha: str
    data_contratacao: date
    enderecos: List['EnderecoCreate'] | None = None


    model_config = ConfigDict(from_attributes=True)



class EnderecoResponse(BaseModel):
    funcionario_id: int
    logradouro: str
    numero: str
    complemento: str | None = None
    bairro: str
    cidade: str
    estado: str
    cep: str

    model_config = ConfigDict(from_attributes=True) 


class EnderecoCreate(BaseModel):
    funcionario_id: int
    logradouro: str
    numero: str
    complemento: str | None = None
    bairro: str
    cidade: str
    estado: str
    cep: str

    model_config = ConfigDict(from_attributes=True) 

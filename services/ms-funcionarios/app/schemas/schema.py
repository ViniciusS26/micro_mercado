from pydantic import BaseModel,field_validator, ConfigDict
from typing import List, Optional
from datetime import date, datetime
from validate_docbr import CPF
from ..core import security

class FuncionarioTokken(BaseModel):
    id: int
    nome: str
    cpf: str
    cargo: str

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
    enderecos: EnderecoCreate


    model_config = ConfigDict(from_attributes=True)

    @field_validator('senha')
    def validar_senha(cls, senha):
        if len(senha) < 8:
            raise ValueError('Senha deve ter pelo menos 8 caracteres')

        hashed_senha = security.get_password_hash(senha)
        return hashed_senha

    @field_validator('cpf')
    def validar_cpf(cls, cpf):
        validador = CPF()
        if not validador.validate(cpf):
            raise ValueError('CPF inválido')
        return cpf

    @field_validator('email')
    def validar_email(cls, email):
        if '@' not in email:
            raise ValueError('Email inválido')
        return email
    
    @field_validator('salario')
    def validar_salario(cls, salario):
        if salario < 1100:
            raise ValueError('Salário não pode ser menor que um salário mínimo (R$1100)')
        return salario




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
    enderecos: List[EnderecoResponse]
    created_at: datetime | None = None
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)



class FuncionarioUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    cargo: Optional[str] = None
    salario: Optional[float] = None
    senha: Optional[str] = None
   

    model_config = ConfigDict(from_attributes=True)



   
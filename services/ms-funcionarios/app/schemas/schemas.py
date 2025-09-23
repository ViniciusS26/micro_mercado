from pydantic import BaseModel,field_validator, ConfigDict
from typing import List
from datetime import date, datetime
from validate_docbr import CPF
from email_validator import validate_email, EmailNotValidError





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

    @field_validator('cpf')
    def validar_cpf(cls, v):
        cpf = CPF()
        if not cpf.validate(v):
            raise ValueError('CPF inválido')
        return cpf.mask(v)

    @field_validator('email')
    def validar_email(cls, v):
        try:
            valid = validate_email(v)
            return valid.email
        except EmailNotValidError as e:
            raise ValueError('Email inválido') from e
    
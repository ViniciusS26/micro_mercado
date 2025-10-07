from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class EnderecoBase(BaseModel):
    rua: str
    cidade: str
    estado: str
    cep: str
    pais: str

class EnderecoCreate(EnderecoBase):
    pass

class Endereco(EnderecoBase):
    id: int

    class Config:
        from_attributes = True

class ProdutoBase(BaseModel):
    nome: str
    descricao: str
    preco: float
    quantidade_estoque: int

class ProdutoCreate(ProdutoBase):
    fornecedor_id: int

class Produto(ProdutoBase):
    id: int
    fornecedor_id: int
    data_criacao: Optional[datetime]
    data_atualizacao: Optional[datetime]

    class Config:
        from_attributes = True

class FornecedorBase(BaseModel):
    nome: str
    cnpj: str
    telefone: str
    email: EmailStr

class FornecedorCreate(FornecedorBase):
    enderecos: EnderecoCreate

class FornecedorUpdate(BaseModel):
    nome: Optional[str]
    telefone: Optional[str]
    email: Optional[EmailStr]
    enderecos: Optional[EnderecoCreate]

class Fornecedor(FornecedorBase):
    id: int
    enderecos: List[Endereco]
    produtos: List[Produto] = []


    class Config:
        from_attributes = True
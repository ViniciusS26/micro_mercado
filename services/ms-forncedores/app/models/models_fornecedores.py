from sqlalchemy import Column, Date,DateTime, ForeignKey, Integer, String, Float, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.database import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    descricao = Column(String)
    preco = Column(Float)
    quantidade_estoque = Column(Integer)
    fornecedor_id = Column(Integer, ForeignKey("fornecedores.id"))
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), onupdate=func.now())

    fornecedor = relationship("Fornecedor", back_populates="produtos")


class Endereco(Base):
    __tablename__ = "enderecos"

    id = Column(Integer, primary_key=True, index=True)
    rua = Column(String)
    cidade = Column(String)
    estado = Column(String)
    cep = Column(String)
    pais = Column(String)
    fornecedor_id = Column(Integer, ForeignKey("fornecedores.id"))
    
    fornecedor = relationship("Fornecedor", back_populates="enderecos")

class Fornecedor(Base):
    __tablename__ = "fornecedores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    cnpj = Column(String, unique=True, index=True)
    enderecos = relationship("Endereco", back_populates="fornecedor")
    telefone = Column(String)
    email = Column(String, unique=True, index=True)
    data_atualizacao = Column(DateTime(timezone=True), onupdate=func.now())

    produtos = relationship("Produto", back_populates="fornecedor")


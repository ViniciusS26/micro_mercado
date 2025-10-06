from sqlalchemy import Column, Date,DateTime, ForeignKey, Integer, String, Float, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.database import Base

""" Classe que representa a tabela de funcionários no banco de dados. """
class Funcionarios(Base):
    __tablename__ = 'funcionarios'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telefone = Column(String(15), nullable=False)
    data_nascimento = Column(Date, nullable=False)
    cargo = Column(String(50), nullable=False)
    salario = Column(Float, nullable=False)
    senha = Column(String(255), nullable=False)
    data_contratacao = Column(Date, default=func.current_date(), nullable=False)
    enderecos = relationship("Enderecos", back_populates="funcionario", cascade="all, delete-orphan")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Enderecos(Base):
    __tablename__ = 'enderecos'

    id = Column(Integer, primary_key=True, index=True)
    funcionario_id = Column(Integer, ForeignKey('funcionarios.id'), nullable=False)
    logradouro = Column(String(100), nullable=False)
    numero = Column(String(10), nullable=False)
    complemento = Column(String(50), nullable=True)
    bairro = Column(String(50), nullable=False)
    cidade = Column(String(50), nullable=False)
    estado = Column(String(2), nullable=False)
    cep = Column(String(10), nullable=False)

    funcionario = relationship("Funcionarios", back_populates="enderecos")
from sqlalchemy import Column, Date,DateTime, ForeignKey, Integer, String, Float, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base

""" Classe que representa a tabela de funcionários no banco de dados. """
class Funcionarios(Base):
    __tablename__ = 'funcionarios'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    rg = Column(String(20), unique=True, nullable=False)
    data_nascimento = Column(Date, nullable=False)
    endereco = Column(String(200), nullable=False)
    telefone = Column(String(15), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    cargo = Column(String(50), nullable=False)
    salario = Column(Float, nullable=False)
    data_contratacao = Column(Date, default=func.current_date(), nullable=False)
    data_demissao = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    dependentes = relationship("Dependentes", back_populates="funcionario", cascade="all, delete-orphan")
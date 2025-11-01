from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.database import Base

class Venda(Base):
    __tablename__ = 'vendas'

    id = Column(Integer, primary_key=True, index=True)
    data_venda = Column(DateTime(timezone=True), server_default=func.now())
    valor_total = Column(Float, nullable=False)
    funcionario_id = Column(Integer, nullable=False) # ID do funcionário do ms-funcionarios
    nome_funcionario = Column(String, nullable=False)
    cpf = Column(String, nullable=False)
    cargo = Column(String, nullable=False)
    itens = relationship("ItemVenda", back_populates="venda", cascade="all, delete-orphan")

class ItemVenda(Base):
    __tablename__ = 'itens_venda'

    id = Column(Integer, primary_key=True, index=True)
    venda_id = Column(Integer, ForeignKey('vendas.id'), nullable=False)
    produto_id = Column(Integer, nullable=False) # ID do produto do ms-produtos
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Float, nullable=False)

    venda = relationship("Venda", back_populates="itens")
from sqlalchemy import Column, Date,DateTime, Integer, String, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..db.database import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    descricao = Column(String, index=True)
    preco = Column(Float, index=True)
    peso = Column(Float, index=True)
    data_fabricacao = Column(Date)
    data_validade = Column(Date)
    data_cadastro = Column(DateTime(timezone=True), server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), onupdate=func.now())


    

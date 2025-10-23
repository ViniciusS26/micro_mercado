from fastapi import APIRouter, Depends, HTTPException, Header, Path
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from ..schemas import schemas
from ..db import querys, connection
from ..models import models_produtos




router = APIRouter(prefix="/produtos")

@router.post("/", response_model=schemas.Produto)
def cadastrar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(connection.get_db)):
    dados_produto = produto.model_dump()
    produto_data = models_produtos.Produto(**dados_produto)
    return querys.criar_produto(db=db, produto=produto_data)

@router.get("/", response_model=List[schemas.Produto])
def listar_produtos(db: Session = Depends(connection.get_db)):
    return querys.obter_produtos(db)

@router.get("/{id}", response_model=schemas.Produto)
def ver_produto(id: int, db: Session = Depends(connection.get_db)):
    # 🔧 ajuste: usar keyword correta esperada por querys.obter_produto_id
    db_produto = querys.obter_produto_id(db, produto_id=id)
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_produto

@router.put("/{id}", response_model=schemas.Produto)
def atualizar_produto(id: int, produto: schemas.ProdutoUpdate, db: Session = Depends(connection.get_db)):
    db_produto = querys.atualiza_produto(db, id=id, produto=produto)
    if db_produto is None:
        raise HTTPException(statusocode=404, detail="Produto não encontrado")
    return db_produto

@router.delete("/{id}", response_model=schemas.Produto)
def deletar_produto(id: int, db: Session = Depends(connection.get_db)):
    # 🔧 ajuste: usar keyword correta esperada por querys.deleta_produto
    db_produto = querys.deleta_produto(db, produto_id=id)
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_produto
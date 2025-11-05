from fastapi import APIRouter, Depends, HTTPException, Header, Path
import httpx
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from schemas import schemas
from db import querys, connection
from models import models_produtos




router = APIRouter(prefix="/produtos")


@router.post("/", response_model=schemas.Produto)
def cadastrar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(connection.get_db)):
    #urls para acessar ms-fornecedores para validar
   
    dados_produto = produto.model_dump()
    produto_data = models_produtos.Produto(**dados_produto)
    return querys.criar_produto(db=db, produto=produto_data)

@router.get("/{titulo}", response_model=schemas.Produto)
def pegar_produto_por_titulo(titulo: str, db: Session = Depends(connection.get_db)):
    db_produto = querys.obter_produto_por_titulo(db, titulo=titulo)
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_produto

@router.get("/", response_model=List[schemas.Produto])
def listar_produtos(db: Session = Depends(connection.get_db)):
    return querys.obter_produtos(db)

@router.get("/{id_produto}", response_model=schemas.Produto)
def ver_produto(id_produto: int, db: Session = Depends(connection.get_db)):
    # 🔧 ajuste: usar keyword correta esperada por querys.obter_produto_id

    db_produto = querys.obter_produto_id(db, id_produto=id_produto)
    print(db_produto)
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_produto

@router.put("/{id_produto}", response_model=schemas.Produto)
def atualizar_produto(id_produto: int, produto: schemas.ProdutoUpdate, db: Session = Depends(connection.get_db)):
    db_produto = querys.atualiza_produto(db, id=id_produto, produto=produto)
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_produto

@router.delete("/{id_produto}", response_model=schemas.Produto)
def deletar_produto(id_produto: int, db: Session = Depends(connection.get_db)):
    # 🔧 ajuste: usar keyword correta esperada por querys.deleta_produto
    db_produto = querys.deleta_produto(db, produto_id=id_produto)
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_produto
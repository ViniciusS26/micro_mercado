from fastapi import APIRouter, Depends, HTTPException, Header, Path
import httpx
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from schemas import ProdutoCreate, ProdutoBase, Produto, ProdutoUpdate
from db.connection import  get_db
from db.querys_produtos import criar_produto, obter_produtos, obter_produto_id, obter_produto_por_titulo, atualiza_produto, deleta_produto, contar_produtos, sum_valor_total
from models import models_produtos




router = APIRouter(prefix="/produtos")


@router.post("/", response_model=ProdutoCreate)
def cadastrar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    
    dados_produto = produto.model_dump()
    produto_data = models_produtos.Produto(**dados_produto)
    return  criar_produto(db=db, produto=produto_data)

@router.get("/{titulo}", response_model=ProdutoBase)
def pegar_produto_por_titulo(titulo: str, db: Session = Depends(get_db)):
    db_produto = obter_produto_por_titulo(db, titulo=titulo)
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_produto

@router.get("/", response_model=List[Produto])
def listar_produtos(db: Session = Depends(get_db)):
    return obter_produtos(db)



@router.put("/{id_produto}", response_model=Produto)
def atualizar_produto(id_produto: int, produto: ProdutoUpdate, db: Session = Depends(get_db)):
    db_produto = atualiza_produto(db, id=id_produto, produto=produto)
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_produto

@router.delete("/{id_produto}", response_model=Produto)
def deletar_produto(id_produto: int, db: Session = Depends(get_db)):
    # 🔧 ajuste: usar keyword correta esperada por querys.deleta_produto
    db_produto = deleta_produto(db, produto_id=id_produto)
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_produto

@router.get("/contar/", response_model=int)
def pegar_total(db: Session = Depends(get_db)):
    return contar_produtos(db)

@router.get("/total_valor/", response_model=float)
def total_valor_produtos(db: Session = Depends(get_db)):
    return sum_valor_total(db)


@router.get("/id/{id_produto}", response_model=Produto)
def pegar_produto_por_id(id_produto: int, db: Session = Depends(get_db)):
    db_produto = obter_produto_id(db, id=id_produto)
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_produto
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from ..schemas import schemas
from ..db import querys, connection
from ..models import models_fornecedores


router = APIRouter(prefix="/fornecedores")

@router.put("/endedereco/{id}", response_model=schemas.Endereco)
def atualizar_endereco(id: int, endereco: schemas.EnderecoCreate, db: Session = Depends(connection.get_db)):
    db_endereco = querys.atualizar_endereco(db, id, endereco=endereco)
    if db_endereco is None:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return db_endereco


@router.post("/produtos", response_model=schemas.Produto)
def criar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(connection.get_db)):
    if querys.buscar_produto_nome(db, nome=produto.nome):
        raise HTTPException(status_code=400, detail="Produto já cadastrado")
    db_produto = models_fornecedores.Produto(**produto.model_dump())
    db_produto = querys.criar_produto(db, db_produto)
    return db_produto

@router.get("/produtos/", response_model=List[schemas.Produto])
def listar_produtos(fornecedor_id: int = None, nome: str = None, db: Session = Depends(connection.get_db)):
    if fornecedor_id:
        return querys.buscar_produtos_por_fornecedor(db, fornecedor_id=fornecedor_id)
    if nome:
        return querys.buscar_produto_nome(db, nome=nome)
    return querys.obter_produtos(db)

@router.put("/produtos/{produto_id}", response_model=schemas.Produto)
def atualizar_produto(produto_id: int, produto: schemas.ProdutoCreate, db: Session = Depends(connection.get_db)):
    db_produto = querys.atualizar_produto(db, produto_id=produto_id, produto=produto)
    if db_produto is None:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return db_produto

@router.get("/produtos", response_model=List[schemas.Produto],summary="listar produtos ")
def listar_produtos(db: Session = Depends(connection.get_db)):
    return querys.obter_produtos(db)

@router.get("/", response_model=List[schemas.Fornecedor])
def listar_fornecedores(db: Session = Depends(connection.get_db)):
    return querys.obter_fornecedores(db)

@router.post("/", response_model=schemas.Fornecedor)
def criar_fornecedor(fornecedor: schemas.FornecedorCreate, db: Session = Depends(connection.get_db)):

    if querys.obter_fornecedor_email(db, email=fornecedor.email):
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    if querys.obter_fornecedor_cnpj(db, cnpj=fornecedor.cnpj):
        raise HTTPException(status_code=400, detail="CNPJ já cadastrado")
    
    dados_fornecedor = fornecedor.model_dump(exclude={"enderecos"})
    db_fornecedor = models_fornecedores.Fornecedor(**dados_fornecedor)

    dado_endereco = fornecedor.enderecos.model_dump()
    db_endereco = models_fornecedores.Endereco(**dado_endereco)


    db_fornecedor.enderecos.append(db_endereco)
    db_fornecedor = querys.criar_fornecedor(db, db_fornecedor)
    
    return db_fornecedor


@router.get("/{fornecedor_id}", response_model=schemas.Fornecedor)
def ler_fornecedor(fornecedor_id: int, db: Session = Depends(connection.get_db)):
    db_fornecedor = querys.obter_fornecedor_id(db, fornecedor_id=fornecedor_id)
    if db_fornecedor is None:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    return db_fornecedor


@router.put("/{id}", response_model=schemas.Fornecedor)
def atualizar_fornecedor(id: int, fornecedor: schemas.FornecedorUpdate, db: Session = Depends(connection.get_db)):
    db_fornecedor = querys.atualizar_fornecedor(db, id=id, fornecedor=fornecedor)
    if db_fornecedor is None:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    return db_fornecedor

@router.delete("/{fornecedor_id}", response_model=schemas.Fornecedor)
def deletar_fornecedor(fornecedor_id: int, db: Session = Depends(connection.get_db)):
    db_fornecedor = querys.deletar_fornecedor(db, fornecedor_id=fornecedor_id)
    if db_fornecedor is None:
        raise HTTPException(status_code=404, detail="Fornecedor não encontrado")
    return db_fornecedor



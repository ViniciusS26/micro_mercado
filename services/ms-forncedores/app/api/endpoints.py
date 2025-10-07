from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from ..schemas import schemas
from ..db import curd, connection
from ..models import models_fornecedores


router = APIRouter(prefix="/fornecedores")

@router.get("/", response_model=List[schemas.Fornecedor])
def listar_fornecedores(db: Session = Depends(connection.get_db)):
    return curd.obter_fornecedores(db)

@router.post("/", response_model=schemas.Fornecedor)
def criar_fornecedor(fornecedor: schemas.FornecedorCreate, db: Session = Depends(connection.get_db)):
    
    if curd.obter_fornecedor_email(db, email=fornecedor.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if curd.obter_fornecedor_cnpj(db, cnpj=fornecedor.cnpj):
        raise HTTPException(status_code=400, detail="CNPJ already registered")
    
    dados_fornecedor = fornecedor.model_dump(exclude={"enderecos"})
    db_fornecedor = models_fornecedores.Fornecedor(**dados_fornecedor)

    dado_endereco = fornecedor.enderecos.model_dump()
    db_endereco = models_fornecedores.Endereco(**dado_endereco)


    db_fornecedor.enderecos.append(db_endereco)
    db_fornecedor = curd.criar_fornecedor(db, db_fornecedor)


    
    return db_fornecedor


@router.get("/{fornecedor_id}", response_model=schemas.Fornecedor)
def ler_fornecedor(fornecedor_id: int, db: Session = Depends(connection.get_db)):
    db_fornecedor = curd.obter_fornecedor_id(db, fornecedor_id=fornecedor_id)
    if db_fornecedor is None:
        raise HTTPException(status_code=404, detail="Fornecedor not found")
    return db_fornecedor


@router.put("/{id}", response_model=schemas.Fornecedor)
def atualizar_fornecedor(id: int, fornecedor: schemas.FornecedorUpdate, db: Session = Depends(connection.get_db)):
    db_fornecedor = curd.atualizar_fornecedor(db, id=id, fornecedor=fornecedor)
    if db_fornecedor is None:
        raise HTTPException(status_code=404, detail="Fornecedor not found")
    return db_fornecedor

@router.delete("/{fornecedor_id}", response_model=schemas.Fornecedor)
def deletar_fornecedor(fornecedor_id: int, db: Session = Depends(connection.get_db)):
    db_fornecedor = curd.deletar_fornecedor(db, fornecedor_id=fornecedor_id)
    if db_fornecedor is None:
        raise HTTPException(status_code=404, detail="Fornecedor not found")
    return db_fornecedor

@router.put("/endedereco/{id}", response_model=schemas.Endereco)
def atualizar_endereco(id: int, endereco: schemas.EnderecoCreate, db: Session = Depends(connection.get_db)):
    db_endereco = curd.atualizar_endereco(db, id, endereco=endereco)
    if db_endereco is None:
        raise HTTPException(status_code=404, detail="Endereço not found")
    return db_endereco
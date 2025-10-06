from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from schemas.schema import FuncionarioCreate, FuncionarioResponse
from sqlalchemy.orm import Session,joinedload
from models.models_funcionarios import Funcionarios, Enderecos
from db.connection import get_db, SessionLocal
from db import crud


router = APIRouter(prefix="/funcionarios")


@router.get("/", response_model=List[FuncionarioResponse])
def obter_funcionario(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    funcionarios = crud.listar_todos_funcionarios(db)[skip: skip + limit]
    return funcionarios

@router.post("/", response_model=FuncionarioResponse)
def criar_funcionario(funcionario: FuncionarioCreate, db: Session = Depends(get_db)):

    if crud.obter_funcionarios_email(db, funcionario.email):
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    if crud.obter_funcionarios_cpf(db, funcionario.cpf):
        raise HTTPException(status_code=400, detail="CPF já cadastrado")
    
    dados_funcionario = funcionario.model_dump(exclude={"enderecos"})
    funcionarios_db = Funcionarios(**dados_funcionario)

    dados_endereco  = funcionario.enderecos.model_dump()
    endereco_db = Enderecos(**dados_endereco)
    funcionarios_db.enderecos.append(endereco_db)

    funcionario_db = crud.criar_funcionario(db, funcionarios_db)

    if not funcionario_db:
        raise HTTPException(status_code=400, detail="Erro ao criar funcionário")
    return funcionario_db
  

@router.put("/{id}", response_model=FuncionarioResponse)
def atualizar_funcionario(id: int, funcionario: FuncionarioResponse, db: Session = Depends(get_db)):
    funcionario_db = crud.atualizar_funcionario(db, id, funcionario)
    if not funcionario_db:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return funcionario_db

@router.delete("/{id}")
def deletar_funcionario(id: int, db: Session = Depends(get_db)):
    funcionario_db = crud.deletar_funcionario(db, id)
    if not funcionario_db:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return {"detail": "Funcionário deletado"}
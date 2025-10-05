from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List
from schemas.schemas import FuncionarioCreate, FuncionarioResponse
from sqlalchemy.orm import Session
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
    funcionario_db = crud.criar_funcionario(db, funcionario)
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
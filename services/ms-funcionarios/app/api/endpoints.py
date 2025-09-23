from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.schemas.schemas import FuncionarioCreate, FuncionarioResponse

router = APIRouter()


# Simulação de banco de dados em memória
funcionarios_db = []

@router.get("/funcionarios", response_model=List[FuncionarioResponse])
def listar_funcionarios():
    return funcionarios_db

@router.get("/funcionarios/{funcionario_id}", response_model=FuncionarioResponse)
def obter_funcionario(funcionario_id: int):
    for funcionario in funcionarios_db:
        if funcionario.id == funcionario_id:
            return funcionario
    raise HTTPException(status_code=404, detail="Funcionário não encontrado")

@router.post("/funcionarios", response_model=FuncionarioResponse)
def criar_funcionario(funcionario: FuncionarioCreate):
    funcionario_db = FuncionarioResponse(**funcionario.dict(), id=len(funcionarios_db) + 1)
    funcionarios_db.append(funcionario_db)
    return funcionario_db

@router.put("/funcionarios/{funcionario_id}", response_model=FuncionarioResponse)
def atualizar_funcionario(funcionario_id: int, funcionario: FuncionarioResponse):
    for idx, f in enumerate(funcionarios_db):
        if f.id == funcionario_id:
            funcionarios_db[idx] = funcionario
            return funcionario
    raise HTTPException(status_code=404, detail="Funcionário não encontrado")

@router.delete("/funcionarios/{funcionario_id}")
def deletar_funcionario(funcionario_id: int):
    for idx, f in enumerate(funcionarios_db):
        if f.id == funcionario_id:
            del funcionarios_db[idx]
            return {"detail": "Funcionário deletado"}
    raise HTTPException(status_code=404, detail="Funcionário não encontrado")
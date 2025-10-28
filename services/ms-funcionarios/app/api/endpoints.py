from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.orm import Session
from ..core import security

from ..schemas.schema import (
    FuncionarioCreate,
    FuncionarioResponse,
    EnderecoResponse,
    EnderecoCreate,
    FuncionarioUpdate,
)
from ..models.models_funcionarios import Funcionarios, Enderecos
from ..db.connection import get_db
from ..db import crud

router = APIRouter(prefix="/funcionarios")


"""Criar rota de login para funcionários de acordo o cpf e senha  """
@router.post("/auth", response_model=security.FuncionarioTokken)
def login_funcionario(cpf: str, senha: str, db: Session = Depends(get_db)):
    funcionario = db.query(Funcionarios).filter(Funcionarios.cpf == cpf).first()
    if not funcionario:
        raise HTTPException(status_code=400, detail="CPF ou senha inválidos")
    if not security.verify_password(senha, funcionario.senha):
        raise HTTPException(status_code=400, detail="CPF ou senha inválidos")

    token_data = {
        "id": funcionario.id,
        "nome": funcionario.nome,
        "cpf": funcionario.cpf,
        "cargo": funcionario.cargo,
    }
   
    return token_data

@router.get("/", response_model=List[FuncionarioResponse])
def obter_funcionario(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    funcionarios = crud.listar_todos_funcionarios(db)[skip : skip + limit]
    return funcionarios

@router.post("/", response_model=FuncionarioResponse)
def criar_funcionario(funcionario: FuncionarioCreate, db: Session = Depends(get_db)):
    # validações únicas
    if crud.obter_funcionarios_email(db, funcionario.email):
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    if crud.obter_funcionarios_cpf(db, funcionario.cpf):
        raise HTTPException(status_code=400, detail="CPF já cadastrado")

    # monta entidades
    dados_funcionario = funcionario.model_dump(exclude={"enderecos"}, exclude_none=True)
    funcionario_db = Funcionarios(**dados_funcionario)

    dados_endereco = funcionario.enderecos.model_dump(exclude_none=True)
    endereco_db = Enderecos(**dados_endereco)

    # VINCULA RELACIONAMENTO SEM DEPENDER DO ID JÁ EXISTIR
    # (o relacionamento vai setar funcionario_id ao persistir)
    funcionario_db.enderecos.append(endereco_db)

    # persiste tudo numa tacada
    funcionario_persistido = crud.criar_funcionario(db, funcionario_db)
    if not funcionario_persistido:
        raise HTTPException(status_code=400, detail="Erro ao criar funcionário")

    return funcionario_persistido
  

@router.put("/{id}", response_model=FuncionarioResponse)
def atualizar_funcionario(id: int, funcionario: FuncionarioUpdate, db: Session = Depends(get_db)):
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

@router.put("/endereco/{id}", response_model=EnderecoResponse)
def atualizar_endereco(id: int, endereco: EnderecoCreate, db: Session = Depends(get_db)):
    # Atualiza campos do endereço. O schema exige funcionario_id/logradouro etc.
    endereco_db = crud.atualizar_endereco(db, id, endereco)
    if not endereco_db:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return endereco_db
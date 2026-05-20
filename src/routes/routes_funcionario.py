from fastapi import APIRouter, Depends, HTTPException

from typing import List
from sqlalchemy.orm import Session
from services import security

from schemas.schema_funcionarios import (
    FuncionarioCreate,
    FuncionarioResponse,
    EnderecoResponse,
    EnderecoUpdate,
    FuncionarioUpdate
)
from models.models_funcionarios import Funcionarios, Enderecos
from db.dependeces import get_db
from db import querys_funcionario

router = APIRouter(prefix="/funcionarios")



@router.post("/auth/")
def login_funcionario(cpf: str, senha: str, db: Session = Depends(get_db)):
    """ Rota de login para funcionários """
    
    # Chama a função de autenticação passando a sessão 'db', o cpf e a senha
    funcionario = security.authenticate_user(db=db, cpf=cpf, password=senha)
   
    # Cria o token usando o CPF do funcionário autenticado
    token = security.create_access_token(data_payload={"sub": funcionario.cpf})
    
    # Retorna o formato padrão esperado pelo OAuth2
    return {"access_token": token, "token_type": "bearer"}

@router.get("/", response_model=List[FuncionarioResponse])
def obter_funcionario(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    funcionarios = querys_funcionario.listar_todos_funcionarios(db)[skip : skip + limit]
    return funcionarios

@router.get("/{id}", response_model=FuncionarioResponse)
def obter_funcionario_por_id(id: int, db: Session = Depends(get_db)):
    funcionario = querys_funcionario.obter_funcionario(db, id)
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return funcionario


@router.post("/", response_model=FuncionarioResponse)
def criar_funcionario(funcionario: FuncionarioCreate, db: Session = Depends(get_db)):
    """ Cria um novo funcionário com endereço associado """
    if querys_funcionario.obter_funcionarios_email(db, funcionario.email):
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    if querys_funcionario.obter_funcionarios_cpf(db, funcionario.cpf):
        raise HTTPException(status_code=400, detail="CPF já cadastrado")

   
    dados_funcionario = funcionario.model_dump(exclude={"enderecos"}, exclude_none=True)
    funcionario_db = Funcionarios(**dados_funcionario)

    dados_endereco = funcionario.enderecos.model_dump(exclude_none=True)
    endereco_db = Enderecos(**dados_endereco)


    funcionario_db.enderecos.append(endereco_db)

    funcionario_persistido = querys_funcionario.criar_funcionario(db, funcionario_db)
    if not funcionario_persistido:
        raise HTTPException(status_code=400, detail="Erro ao criar funcionário")

    return funcionario_persistido
  

@router.put("/{id}", response_model=FuncionarioResponse)
def atualizar_funcionario(id: int, funcionario: FuncionarioUpdate, db: Session = Depends(get_db)):
    """ Atualiza os dados de um funcionário existente """
    funcionario_db = querys_funcionario.atualizar_funcionario(db, id, funcionario)
    if not funcionario_db:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return funcionario_db

@router.delete("/{id}")
def deletar_funcionario(id: int, db: Session = Depends(get_db)):
    """ Deleta um funcionário existente """
    funcionario_db = querys_funcionario.deletar_funcionario(db, id)
    if not funcionario_db:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return {"detail": "Funcionário deletado"}

@router.put("/endereco/{id}", response_model=EnderecoResponse)
def atualizar_endereco(id: int, endereco: EnderecoUpdate, db: Session = Depends(get_db)):
    """ Atualiza os dados de um endereço existente """
    endereco_db = querys_funcionario.atualizar_endereco(db, id, endereco)
    if not endereco_db:
        raise HTTPException(status_code=404, detail="Endereço não encontrado")
    return endereco_db
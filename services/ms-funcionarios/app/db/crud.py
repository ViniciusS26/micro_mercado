from sqlalchemy.orm import Session
from models.models_funcionarios import Funcionarios, Enderecos
from schemas.schemas import FuncionarioCreate, EnderecoCreate


def listar_todos_funcionarios(db: Session):
    return db.query(Funcionarios).all()

def obter_funcionario(db: Session, id: int):
    return db.query(Funcionarios).filter(Funcionarios.id == id).first()

def obter_funcionarios_email(db: Session, email: str):
    return db.query(Funcionarios).filter(Funcionarios.email == email).all()


def obter_funcionarios_cpf(db: Session, cpf: str):
    return db.query(Funcionarios).filter(Funcionarios.cpf == cpf).all()

def ataulizar_funcionario(db: Session, id: int, funcionario: FuncionarioCreate):
    funcionario_db = db.query(Funcionarios).filter(Funcionarios.id == id).first()
    if funcionario_db:
        for key, value in funcionario.dict().items():
            setattr(funcionario_db, key, value)
        db.commit()
        db.refresh(funcionario_db)
    return funcionario_db

def deletar_funcionario(db: Session, id: int):
    funcionario_db = db.query(Funcionarios).filter(Funcionarios.id == id).first()
    if funcionario_db:
        db.delete(funcionario_db)
        db.commit()
    return funcionario_db




def criar_funcionario(db: Session, funcionario: FuncionarioCreate):
    funcionario_db = Funcionarios(**funcionario.dict())
    db.add(funcionario_db)
    db.commit()
    db.refresh(funcionario_db)
    return funcionario_db


def atualizar_endereco(db: Session, id: int, endereco: EnderecoCreate):
    endereco_db = db.query(Enderecos).filter(Enderecos.id == id).first()
    if endereco_db:
        for key, value in endereco.dict().items():
            setattr(endereco_db, key, value)
        db.commit()
        db.refresh(endereco_db)
    return endereco_db

def deletar_endereco(db: Session, id: int):
    endereco_db = db.query(Enderecos).filter(Enderecos.id == id).first()
    if endereco_db:
        db.delete(endereco_db)
        db.commit()
    return endereco_db


def obter_enderecos_funcionario(db: Session, funcionario_id: int):
    return db.query(Enderecos).filter(Enderecos.funcionario_id == funcionario_id).all()


def criar_endereco(db: Session, endereco: EnderecoCreate):
    endereco_db = Enderecos(**endereco.dict())
    db.add(endereco_db)
    db.commit()
    db.refresh(endereco_db)
    return endereco_db
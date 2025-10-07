from sqlalchemy.orm import Session, joinedload
from ..models import models_fornecedores as models
from ..schemas.schemas import FornecedorCreate, FornecedorUpdate, ProdutoCreate, EnderecoCreate

def obter_fornecedores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Fornecedor).options(joinedload(models.Fornecedor.enderecos), joinedload(models.Fornecedor.produtos)).offset(skip).limit(limit).all()


def obter_fornecedor_email(db: Session, email: str):
    return db.query(models.Fornecedor).filter(models.Fornecedor.email == email).first()

def obter_fornecedor_cnpj(db: Session, cnpj: str):
    return db.query(models.Fornecedor).filter(models.Fornecedor.cnpj == cnpj).first()

def obter_fornecedor_id(db: Session, fornecedor_id: int):
    return db.query(models.Fornecedor).filter(models.Fornecedor.id == fornecedor_id).first()

def criar_fornecedor(db: Session, fornecedor: FornecedorCreate):
  
    db.add(fornecedor)
    db.commit()
    db.refresh(fornecedor)
    return fornecedor

def atualizar_fornecedor(db: Session, fornecedor_id: int, fornecedor: FornecedorUpdate):
    db_fornecedor = obter_fornecedores(db, fornecedor_id)
    
    if db_fornecedor:
        update_data = fornecedor.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_fornecedor, key, value)
            db.commit()
            db.refresh(db_fornecedor)

    return db_fornecedor


def criar_endereco(db: Session, endereco: EnderecoCreate):
    
    db.add(endereco)
    db.commit()
    db.refresh(endereco)
    return endereco

def atualizar_endereco(db: Session, id: int, endereco: EnderecoCreate):
    db_endereco = db.query(models.Endereco).filter(models.Endereco.id == id).first()

    if db_endereco:
        update_data = endereco.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_endereco, key, value)
        db.commit()
        db.refresh(db_endereco)
    
    return db_endereco

def deletar_fornecedor(db: Session, fornecedor_id: int):
    db_fornecedor = obter_fornecedores(db, fornecedor_id)
    if db_fornecedor:
        db.delete(db_fornecedor)
        db.commit()
    return db_fornecedor

def criar_produto(db: Session, produto: ProdutoCreate):
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto

def buscar_produtos_por_fornecedor(db: Session, fornecedor_id: int):
    return db.query(models.Produto).filter(models.Produto.fornecedor_id == fornecedor_id).all()

def buscar_produto_nome(db: Session, nome: str):
    return db.query(models.Produto).filter(models.Produto.nome.ilike(f"%{nome}%")).all()

def buscar_produto_id(db: Session, produto_id: int):
    return db.query(models.Produto).filter(models.Produto.id == produto_id).first()

def atualizar_produto(db: Session, produto_id: int, produto: ProdutoCreate):
    db_produto = buscar_produto_id(db, produto_id)
    
    if db_produto:
        update_data = produto.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_produto, key, value)
        db.commit()
        db.refresh(db_produto)
    
    return db_produto

def deletar_produto(db: Session, produto_id: int):
    db_produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if db_produto:
        db.delete(db_produto)
        db.commit()
    return db_produto


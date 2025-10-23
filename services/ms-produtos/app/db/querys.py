from sqlalchemy.orm import Session, joinedload
from ..models import models_produtos
from sqlalchemy.exc import IntegrityError
from ..schemas import schemas
from sqlalchemy import func


def criar_produto(db: Session, produto):
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto

def obter_produtos(db: Session):
    return db.query(models_produtos.Produto).all()

def obter_produto_id(db: Session, produto_id: int):
    return db.query(models_produtos.Produto).filter(models_produtos.Produto.id == produto_id).first()

def atualiza_produto(db: Session, id: int, produto):
    db_produto = db.query(models_produtos.Produto).filter(models_produtos.Produto.id == id).first()
    if db_produto:
        # já ajustado anteriormente para não sobrescrever com None e não mexer em id
        data = produto.model_dump(exclude_unset=True, exclude_none=True)
        data.pop("id", None)
        for key, value in data.items():
            setattr(db_produto, key, value)
        db.commit()
        db.refresh(db_produto)
    return db_produto

def deleta_produto(db: Session, produto_id: int):
    db_produto = obter_produto_id(db, produto_id)
    if db_produto:
        db.delete(db_produto)
        db.commit()
        # não fazer refresh em objeto deletado
    return db_produto

def contar_produtos(db: Session):
    return db.query(models_produtos.Produto).count()



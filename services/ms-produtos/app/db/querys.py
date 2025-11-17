from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from models.models_produtos import Produto


def criar_produto(db: Session, produto):
    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto

def obter_produtos(db: Session):
    return db.query(Produto).all()

def obter_produto_id(db: Session, id: int):
    return db.query(Produto).filter(Produto.id == id).first()

def obter_produto_por_titulo(db: Session, titulo: str):
    return db.query(Produto).filter(Produto.titulo == titulo).first()

def atualiza_produto(db: Session, id: int, produto):
    db_produto = db.query(Produto).filter(Produto.id == id).first()
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
    return db_produto

def contar_produtos(db: Session):
    return db.query(Produto).count()


def sum_valor_total(db: Session):
    total = db.query(func.sum(Produto.peso)).scalar()
    return total if total is not None else 0


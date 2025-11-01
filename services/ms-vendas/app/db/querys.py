from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from datetime import date, timedelta
from ..models import models_vendas as models
from ..schemas import schemas_vendas as schemas

from typing import Any


def criar_venda(db: Session, venda: schemas.VendaCreate):
    """
    Cria uma nova venda com seus itens associados.
    """
    
    # 1. Calcula o valor total (não vem no schema VendaCreate)
    valor_total = sum(item.quantidade * item.preco_unitario for item in venda.itens)

    # 2. Cria os objetos ItemVenda (models) a partir dos schemas
    db_itens = [
        models.ItemVenda(
            produto_id=item.produto_id,
            quantidade=item.quantidade,
            preco_unitario=item.preco_unitario
        ) for item in venda.itens
    ]

    # 3. Cria o objeto Venda (model) principal
    db_venda = models.Venda(
        **venda.model_dump(exclude={"itens"}),
        valor_total=valor_total,
        itens=db_itens  
    )
    db.add(db_venda)
    db.commit()
    db.refresh(db_venda)
    
    return db_venda


def listar_vendas(
    db: Session,
    data_inicio: date | None = None,
    data_fim: date | None = None,
    skip: int = 0,
    limit: int = 100
):
    """
    Lista todas as vendas com estatísticas, filtros por data e paginação.
    """
    query_base = db.query(models.Venda)

    if data_inicio:
        query_base = query_base.filter(models.Venda.data_venda >= data_inicio)
    if data_fim:
        query_base = query_base.filter(models.Venda.data_venda < data_fim + timedelta(days=1))

    total_registros = query_base.count()

    valor_total_periodo_query = query_base.with_entities(func.sum(models.Venda.valor_total)).scalar()
    valor_total_periodo = valor_total_periodo_query or 0.0

    total_produtos_periodo_query = query_base.join(models.ItemVenda).with_entities(func.sum(models.ItemVenda.quantidade)).scalar()
    total_produtos_periodo = total_produtos_periodo_query or 0

    estatisticas_obj = schemas.PaginaVendasStats(
        total_registros=total_registros,
        valor_total_periodo=valor_total_periodo,
        total_produtos_periodo=total_produtos_periodo
    )

    vendas_db = query_base.order_by(models.Venda.data_venda.desc()).options(joinedload(models.Venda.itens)).offset(skip).limit(limit).all()

    pagina_data = {
        "estatisticas": estatisticas_obj,
        "vendas": vendas_db
    }
    
    return schemas.PaginaVendas.model_validate(pagina_data)


def obter_venda_por_id(db: Session, venda_id: int):
    """
    Busca uma única venda pelo seu ID, incluindo os itens.
    """
    return db.query(models.Venda).options(joinedload(models.Venda.itens)).filter(models.Venda.id == venda_id).first()

def listar_vendas_por_funcionario(db: Session, funcionario_id: int):
    """
    Busca todas as vendas realizadas por um funcionário específico.
    """
    return db.query(models.Venda).options(joinedload(models.Venda.itens)).filter(models.Venda.funcionario_id == funcionario_id).all()

def obter_relatorio_por_funcionario(
    db: Session, 
    funcionario_id: int,
    data_inicio: date | None = None,
    data_fim: date | None = None,
    skip: int = 0,
    limit: int = 10
):
    """
    Gera um relatório completo de vendas para um funcionário,
    com estatísticas, filtros e paginação.
    """
    
    query_base = db.query(models.Venda).filter(models.Venda.funcionario_id == funcionario_id)

    if data_inicio:
        query_base = query_base.filter(models.Venda.data_venda >= data_inicio)
    if data_fim:
        query_base = query_base.filter(models.Venda.data_venda < data_fim + timedelta(days=1))

    total_vendas = query_base.count()

    valor_total_vendido_query = query_base.with_entities(func.sum(models.Venda.valor_total)).scalar()
    valor_total_vendido = valor_total_vendido_query or 0.0

    total_produtos_vendidos_query = query_base.join(models.ItemVenda).with_entities(func.sum(models.ItemVenda.quantidade)).scalar()
    total_produtos_vendidos = total_produtos_vendidos_query or 0

    estatisticas_obj = schemas.RelatorioFuncionarioStats(
        total_vendas=total_vendas,
        valor_total_vendido=valor_total_vendido,
        total_produtos_vendidos=total_produtos_vendidos
    )

    vendas_db = query_base.options(joinedload(models.Venda.itens)).offset(skip).limit(limit).all()

    relatorio_data = {
        "estatisticas": estatisticas_obj,
        "vendas": vendas_db
    }

    return schemas.RelatorioFuncionario.model_validate(relatorio_data)


def deletar_venda(db: Session, venda_id: int):
    """
    Deleta uma venda do banco de dados pelo seu ID.
    """
    db_venda = db.query(models.Venda).filter(models.Venda.id == venda_id).first()

    if db_venda:
        db.delete(db_venda)
        db.commit()
    
    return db_venda

def atualizar_venda(db: Session, venda_id: int, venda_update: schemas.VendaUpdate):
    """
    Atualiza uma venda existente, substituindo os itens e recalculando o total.
    """
    db_venda = db.query(models.Venda).options(joinedload(models.Venda.itens)).filter(models.Venda.id == venda_id).first()

    if not db_venda:
        return None

    db_venda.itens.clear()
    db.flush()

    db_venda.funcionario_id = venda_update.funcionario_id  # type: ignore
    
    novo_valor_total = sum(item.quantidade * item.preco_unitario for item in venda_update.itens)
    db_venda.valor_total = novo_valor_total  # type: ignore

    for item_schema in venda_update.itens:
        novo_item = models.ItemVenda(
            **item_schema.model_dump(),
            venda_id=db_venda.id
        )
        db.add(novo_item)

    db.commit()
    db.refresh(db_venda)
    
    return db_venda
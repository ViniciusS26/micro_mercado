from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from ..schemas import schemas_vendas as schemas
from ..db import querys
from ..db.connection import get_db

router = APIRouter(prefix="/vendas")

@router.post("/", response_model=schemas.Venda)
def criar_nova_venda(venda: schemas.VendaCreate, db: Session = Depends(get_db)):
    """
    Cria uma nova venda com uma lista de produtos.
    """
    return querys.criar_venda(db=db, venda=venda)


@router.get("/", response_model=schemas.PaginaVendas)
def ler_vendas(
    db: Session = Depends(get_db),
    data_inicio: date | None = None,
    data_fim: date | None = None,
    skip: int = 0,
    limit: int = 100
):
    """
    Retorna uma página de vendas com estatísticas, 
    permitindo filtro por data.
    """
    return querys.listar_vendas(
        db=db, 
        data_inicio=data_inicio, 
        data_fim=data_fim, 
        skip=skip, 
        limit=limit
    )


@router.get("/{venda_id}", response_model=schemas.Venda)
def ler_venda_por_id(venda_id: int, db: Session = Depends(get_db)):
    """
    Busca e retorna uma venda específica pelo seu ID.
    """
    db_venda = querys.obter_venda_por_id(db, venda_id=venda_id)
    if db_venda is None:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return db_venda

@router.get(
    "/funcionario/{funcionario_id}", 
    response_model=schemas.RelatorioFuncionario
)
def gerar_relatorio_de_funcionario(
    funcionario_id: int, 
    data_inicio: date | None = None,
    data_fim: date | None = None,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Gera um relatório de vendas para um funcionário com estatísticas,
    filtros por data e paginação.
    """
    relatorio = querys.obter_relatorio_por_funcionario(
        db=db, 
        funcionario_id=funcionario_id,
        data_inicio=data_inicio,
        data_fim=data_fim,
        skip=skip,
        limit=limit
    )
    return relatorio

@router.delete("/{venda_id}", response_model=schemas.Venda)
def deletar_venda_por_id(venda_id: int, db: Session = Depends(get_db)):
    """
    Deleta uma venda específica pelo seu ID.
    """
    db_venda = querys.deletar_venda(db, venda_id=venda_id)
    if db_venda is None:
        raise HTTPException(status_code=404, detail="Venda não encontrada")
    return db_venda

@router.put("/{venda_id}", response_model=schemas.Venda)
def atualizar_venda_por_id(
    venda_id: int, 
    venda_update: schemas.VendaUpdate, 
    db: Session = Depends(get_db)
):
    """
    Atualiza uma venda existente, substituindo completamente seus itens.
    """
    db_venda = querys.atualizar_venda(db, venda_id=venda_id, venda_update=venda_update)
    if db_venda is None:
        raise HTTPException(status_code=404, detail="Venda não encontrada para atualização")
    return db_venda
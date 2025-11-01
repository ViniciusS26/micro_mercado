from fastapi import APIRouter, Depends, HTTPException
import httpx
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from ..schemas import schemas_vendas as schemas
from ..db import querys
from ..db.connection import get_db

router = APIRouter(prefix="/vendas", tags=["Vendas"])



async def buscar_produtos_service(tituloProduto: str):
    """função para acessar o serviço de produtos para pegar os produtos e salvar nos itens da venda"""

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"http://localhost:8002/api/v1/produtos/{tituloProduto}"
            )
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return httpx.Response(status_code=404)
        except httpx.HTTPStatusError as exec:
            raise HTTPException(status_code=503, detail=f"Erro ao contactar serviço de produtos: {exec}")
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Erro ao contactar serviço de produtos: {exc}")




async def buscar_funcionario_service(id_funcionario:int):
    """função para acessar o serviço de funcionários para pegar os funcionários e salvar na venda"""

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"http://localhost:8001/api/v1/funcionarios/{id_funcionario}"
            )
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                return httpx.Response(status_code=404)
        except httpx.HTTPStatusError as exec:
            raise HTTPException(status_code=503, detail=f"Erro ao contactar serviço de funcionários: {exec}")
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Erro ao contactar serviço de funcionários: {exc}")



@router.get("/produtos/{tituloProduto}", response_model=schemas.Produto)
async def obter_produto_por_titulo(tituloProduto: str):
    """Rota para obter produto por título via ms-produtos"""
    produto_response = await buscar_produtos_service(tituloProduto)
    if isinstance(produto_response, httpx.Response) and produto_response.status_code == 404:
        raise HTTPException(status_code=404, detail="Produto não encontrado no serviço de produtos")
    return produto_response

@router.post("/{tituloProduto}", response_model=schemas.Venda)
async def criar_nova_venda(tituloProduto: str, id_funcionario: int, db: Session = Depends(get_db)):
    """Cria uma nova venda, validando produtos via ms-produtos"""
    produto_response = await buscar_produtos_service(tituloProduto)
    funcionario_response = await buscar_funcionario_service(id_funcionario)

    if isinstance(produto_response, httpx.Response) and produto_response.status_code == 404:
        raise HTTPException(status_code=404, detail="Produto não encontrado no serviço de produtos")

    if isinstance(funcionario_response, httpx.Response) and funcionario_response.status_code == 404:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado no serviço de funcionários")
    
    # 1. Mapeia a resposta do produto para o schema Produto
    try:
        produto_schema = schemas.Produto(**produto_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Resposta inesperada do serviço de produtos: {e}")

    # 2. Cria o schema do ItemVenda (o item que foi vendido)
    item_para_venda = schemas.ItemVendaCreate(
        produto_id=produto_schema.id,
        quantidade=1,  # Você definiu como 1 no seu código
        preco_unitario=produto_schema.preco
    )

    # 3. Cria o schema da VendaCreate, já incluindo o item na lista "itens"
    try:
        venda_schema_create = schemas.VendaCreate(
            funcionario_id=funcionario_response["id"],
            nome_funcionario=funcionario_response.get("nome", "Nome não encontrado"),
            cpf=funcionario_response.get("cpf", "CPF não encontrado"),
            cargo=funcionario_response.get("cargo", "Cargo não encontrado"),
            itens=[item_para_venda]  # <-- AQUI ESTÁ A MUDANÇA PRINCIPAL
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao criar schema da Venda: {e}")

    # 4. Passa o schema da Venda (que agora contém os itens) para a função de query
    return querys.criar_venda(db=db, venda=venda_schema_create)



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
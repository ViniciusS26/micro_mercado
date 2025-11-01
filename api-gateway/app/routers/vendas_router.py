import httpx
from fastapi import APIRouter, Request, HTTPException, Response, Query, Path, Body
from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict

from ..core.config import settings

router = APIRouter()

# =======================
#   MODELOS P/ DOCS
# =======================

class NovaVendaCreate(BaseModel):
    model_config = ConfigDict(extra="allow")  # permite campos extras sem quebrar
    titulo_produto: str = Field(..., description="Título do produto a ser vendido")
    id_funcionario: int = Field(..., description="ID do funcionário que está vendendo")


class ItemCreate(BaseModel):
    model_config = ConfigDict(extra="allow")  # permite campos extras sem quebrar
    produto_id: int = Field(..., description="ID do produto")
    qtd: int = Field(..., ge=1, description="Quantidade do item")
    preco_unitario: Optional[float] = Field(None, ge=0, description="Preço unitário (opcional)")

class VendaCreate(BaseModel):
    model_config = ConfigDict(extra="allow")
    cliente_id: int = Field(..., description="ID do cliente")
    itens: List[ItemCreate] = Field(..., description="Lista de itens da venda")
    data: Optional[date] = Field(None, description="Data da venda (opcional)")

class ItemUpdate(BaseModel):
    model_config = ConfigDict(extra="allow")
    produto_id: int = Field(..., description="ID do produto")
    qtd: int = Field(..., ge=1, description="Quantidade do item")
    preco_unitario: Optional[float] = Field(None, ge=0, description="Preço unitário (opcional)")

class VendaUpdate(BaseModel):
    model_config = ConfigDict(extra="allow")
    # Atualização substitutiva completa (espelhando o ms-vendas):
    itens: List[ItemUpdate] = Field(..., description="Nova lista completa de itens")
    cliente_id: Optional[int] = Field(None, description="Atualizar o cliente (opcional)")
    data: Optional[date] = Field(None, description="Atualizar a data (opcional)")

# =======================
#   HELPERS DE PROXY
# =======================

# Headers que não devem ser repassados no proxy (hop-by-hop)
HOP_BY_HOP = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailers",
    "transfer-encoding",
    "upgrade",
    "content-length",
}

def _make_proxy_response(r: httpx.Response) -> Response:
    """
    Constrói uma Response do FastAPI a partir de um httpx.Response,
    materializando o corpo (sem streaming) e filtrando headers hop-by-hop.
    """
    headers = {k: v for k, v in r.headers.items() if k.lower() not in HOP_BY_HOP}
    return Response(
        status_code=r.status_code,
        content=r.content,  # corpo já bufferizado (evita StreamConsumed)
        headers=headers,
        media_type=r.headers.get("content-type"),
    )

async def _forward_request(
    request: Request,
    path: str,
    *,
    extra_params: dict | None = None,
    json_body: dict | None = None,
) -> Response:
    """
    Encaminha a requisição atual para o ms-vendas, usando caminho RELATIVO
    à base do serviço configurada em settings.MS_VENDAS_URL.
    Se 'json_body' for fornecido, ele é enviado como JSON (e ignoramos o body bruto).
    """
    target_path = path.lstrip("/")  # garante que é relativo
    method = request.method
    headers = dict(request.headers)
    params = dict(request.query_params)

    # inclui parâmetros explícitos vindos da assinatura (para documentação)
    if extra_params:
        for k, v in extra_params.items():
            if isinstance(v, date):
                params[k] = v.isoformat()
            elif v is not None:
                params[k] = v
            else:
                params.pop(k, None)

    # Remove headers problemáticos que podem conflitar
    headers.pop("host", None)
    headers.pop("content-length", None)
    headers.pop("transfer-encoding", None)

    try:
        async with httpx.AsyncClient(
            base_url=settings.MS_VENDAS_URL, timeout=10.0
        ) as client:
            if json_body is not None:
                r = await client.request(
                    method=method,
                    url=target_path,
                    headers=headers,
                    params=params,
                    json=json_body,  # garante Content-Type e serialização
                )
            else:
                # Fallback: repassa o corpo bruto
                content = await request.body()
                r = await client.request(
                    method=method,
                    url=target_path,
                    headers=headers,
                    params=params,
                    content=content,
                )
        return _make_proxy_response(r)

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Timeout ao contactar serviço de vendas")
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail=f"Erro ao contactar serviço de vendas: {exc}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no gateway (vendas): {e}")

# =======================
#   ROTAS (ESPELHO)
# =======================

@router.get("/produtos/{tituloProduto}", summary="Obter produto por título")
async def obter_produto_por_titulo_proxy(
    request: Request,
    tituloProduto: str = Path(..., description="Título do produto"),
):
    """
    GET /api/v1/vendas/produtos/{tituloProduto}
    Obtém produto por título via ms-produtos (espelho do ms-vendas).
    """
    return await _forward_request(request, f"produtos/{tituloProduto}")


@router.post("/", summary="Criar venda")
async def criar_venda_proxy(
    request: Request,
    body: NovaVendaCreate = Body(...)
):
    """
    POST /api/v1/vendas/
    Cria uma nova venda (espelho do ms-vendas).
    """
  
    json_body = body.model_dump(mode="json", exclude_none=True)
    return await _forward_request(
        request,
        "",
        json_body=json_body
    )


@router.get("/", summary="Listar vendas")
async def ler_vendas_proxy(
    request: Request,
    data_inicio: date | None = Query(default=None, description="Data inicial (YYYY-MM-DD)"),
    data_fim: date | None = Query(default=None, description="Data final (YYYY-MM-DD)"),
    skip: int = Query(default=0, ge=0, description="Offset/paginação"),
    limit: int = Query(default=100, ge=1, le=1000, description="Tamanho da página"),
):
    """
    GET /api/v1/vendas/
    Lista vendas com filtros por data e paginação (espelho do ms-vendas).
    """
    extra_params = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "skip": skip,
        "limit": limit,
    }
    return await _forward_request(request, "", extra_params=extra_params)

@router.get("/{venda_id:int}", summary="Obter venda por ID")
async def ler_venda_por_id_proxy(
    request: Request,
    venda_id: int = Path(..., ge=1, description="ID da venda"),
):
    """
    GET /api/v1/vendas/{venda_id}
    Busca venda específica por ID.
    """
    return await _forward_request(request, f"{venda_id}")

@router.get("/funcionario/{funcionario_id:int}", summary="Relatório por funcionário")
async def gerar_relatorio_funcionario_proxy(
    request: Request,
    funcionario_id: int = Path(..., ge=1, description="ID do funcionário"),
    data_inicio: date | None = Query(default=None, description="Data inicial (YYYY-MM-DD)"),
    data_fim: date | None = Query(default=None, description="Data final (YYYY-MM-DD)"),
    skip: int = Query(default=0, ge=0, description="Offset/paginação"),
    limit: int = Query(default=10, ge=1, le=1000, description="Tamanho da página"),
):
    """
    GET /api/v1/vendas/funcionario/{funcionario_id}
    Gera relatório de vendas por funcionário com filtros e paginação.
    """
    extra_params = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "skip": skip,
        "limit": limit,
    }
    return await _forward_request(request, f"funcionario/{funcionario_id}", extra_params=extra_params)

@router.delete("/{venda_id:int}", summary="Deletar venda")
async def deletar_venda_proxy(
    request: Request,
    venda_id: int = Path(..., ge=1, description="ID da venda"),
):
    """
    DELETE /api/v1/vendas/{venda_id}
    Remove venda por ID.
    """
    return await _forward_request(request, f"{venda_id}")

@router.put("/{venda_id:int}", summary="Atualizar venda por ID")
async def atualizar_venda_proxy(
    request: Request,
    venda_id: int = Path(..., ge=1, description="ID da venda"),
    body: VendaUpdate = Body(...),   # <- obrigatório e tipado (corrige mypy)
):
    """
    PUT /api/v1/vendas/{venda_id}
    Atualiza venda por ID (substituição completa de itens; espelho do ms-vendas).
    """
    json_body = body.model_dump(exclude_none=True)
    return await _forward_request(request, f"{venda_id}", json_body=json_body)
import httpx
from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    Response,
    Path,
    Body,
)
from typing import Optional
from datetime import date, datetime
from pydantic import BaseModel, Field, ConfigDict

from ..core.config import settings

router = APIRouter()

# =======================
#   MODELOS P/ DOCS (espelho do ms-produtos)
#   Exemplos alinhados ao payload do serviço:
#   {
#     "titulo": "string",
#     "descricao": "string",
#     "preco": 0,
#     "peso": 0,
#     "data_fabricacao": "2025-10-23",
#     "data_validade": "2025-10-23",
#     "data_cadastro": "2025-10-23T14:42:31.947Z",
#     "data_atualizacao": "2025-10-23T14:42:31.947Z"
#   }
# =======================

class ProdutoBase(BaseModel):
    model_config = ConfigDict(extra="allow")

    titulo: Optional[str] = Field(None, description="Título do produto")
    descricao: Optional[str] = Field(None, description="Descrição do produto")
    preco: Optional[float] = Field(None, ge=0, description="Preço do produto")
    peso: Optional[float] = Field(None, ge=0, description="Peso (kg)")
    data_fabricacao: Optional[date] = Field(None, description="Data de fabricação (YYYY-MM-DD)")
    data_validade: Optional[date] = Field(None, description="Data de validade (YYYY-MM-DD)")
    data_cadastro: Optional[datetime] = Field(None, description="Carimbo de criação (ISO 8601)")
    data_atualizacao: Optional[datetime] = Field(None, description="Carimbo de atualização (ISO 8601)")

class ProdutoCreate(ProdutoBase):
    # Ajuste os obrigatórios conforme seu schemas.ProdutoCreate real:
    titulo: str = Field(..., description="Título do produto")
    preco: float = Field(..., ge=0, description="Preço do produto")

class ProdutoUpdate(ProdutoBase):
    # Todos opcionais no update
    pass

# =======================
#   HELPERS DE PROXY
# =======================

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
    headers = {k: v for k, v in r.headers.items() if k.lower() not in HOP_BY_HOP}
    return Response(
        status_code=r.status_code,
        content=r.content,
        headers=headers,
        media_type=r.headers.get("content-type"),
    )

async def _forward_request(
    request: Request,
    path: str,
    *,
    json_body: dict | None = None,
) -> Response:
    """
    Encaminha a requisição para o ms-produtos usando caminho RELATIVO
    à base configurada em settings.MS_PRODUTOS_URL.
    """
    target_path = path.lstrip("/")
    method = request.method
    headers = dict(request.headers)
    params = dict(request.query_params)

    headers.pop("host", None)
    headers.pop("content-length", None)
    headers.pop("transfer-encoding", None)

    try:
        async with httpx.AsyncClient(
            base_url=settings.MS_PRODUTOS_URL, timeout=10.0
        ) as client:
            if json_body is not None:
                r = await client.request(
                    method=method,
                    url=target_path,
                    headers=headers,
                    params=params,
                    json=json_body,
                )
            else:
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
        raise HTTPException(status_code=504, detail="Timeout ao contactar serviço de produtos")
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail=f"Erro ao contactar serviço de produtos: {exc}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no gateway (produtos): {e}")

# =======================
#   ROTAS (ESPELHO ms-produtos)
#   Base real do serviço: /api/v1/produtos
# =======================

@router.post("/", summary="Cadastrar produto")
async def cadastrar_produto_proxy(
    request: Request,
    body: ProdutoCreate = Body(...),
):
    """
    POST /api/v1/produtos/
    Cadastra um produto (espelho do ms-produtos).
    """
    # mode="json" -> serializa date/datetime em ISO automaticamente
    json_body = body.model_dump(mode="json", exclude_none=True)
    return await _forward_request(request, "", json_body=json_body)

@router.get("/", summary="Listar produtos")
async def listar_produtos_proxy(request: Request):
    """
    GET /api/v1/produtos/
    Lista todos os produtos.
    """
    return await _forward_request(request, "")

@router.get("/{titulo}", summary="Listar produtos por título")
async def listar_produtos_por_titulo_proxy(
    request: Request,
    titulo: str = Path(..., description="Título do produto"),
):
    """
    GET /api/v1/produtos/
    Lista todos os produtos.
    """
    return await _forward_request(request, f"/{titulo}")


@router.get("/{id:int}", summary="Ver produto por ID")
async def ver_produto_proxy(
    request: Request,
    id: int = Path(..., ge=1, description="ID do produto"),
):
    """
    GET /api/v1/produtos/{id}
    Retorna um produto específico por ID.
    """
    return await _forward_request(request, f"{id}")

@router.put("/{id:int}", summary="Atualizar produto")
async def atualizar_produto_proxy(
    request: Request,
    id: int = Path(..., ge=1, description="ID do produto"),
    body: ProdutoUpdate = Body(...),
):
    """
    PUT /api/v1/produtos/{id}
    Atualiza um produto (campos parciais ou totais).
    """
    json_body = body.model_dump(mode="json", exclude_none=True)
    return await _forward_request(request, f"{id}", json_body=json_body)

@router.delete("/{id:int}", summary="Deletar produto")
async def deletar_produto_proxy(
    request: Request,
    id: int = Path(..., ge=1, description="ID do produto"),
):
    """
    DELETE /api/v1/produtos/{id}
    Deleta um produto por ID.
    """
    return await _forward_request(request, f"{id}")
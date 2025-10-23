import httpx
from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    Response,
    Query,
    Path,
    Body,
)
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

from ..core.config import settings

router = APIRouter()

# =======================
#   MODELOS P/ DOCS (espelho flexível)
# =======================

class EnderecoCreate(BaseModel):
    model_config = ConfigDict(extra="allow")
    rua: Optional[str] = Field(None, description="Rua")
    numero: Optional[str] = Field(None, description="Número")
    bairro: Optional[str] = Field(None, description="Bairro")
    cidade: Optional[str] = Field(None, description="Cidade")
    estado: Optional[str] = Field(None, description="Estado")
    cep: Optional[str] = Field(None, description="CEP")

class FornecedorCreate(BaseModel):
    model_config = ConfigDict(extra="allow")
    nome: str = Field(..., description="Nome do fornecedor")
    email: str = Field(..., description="E-mail do fornecedor")
    cnpj: str = Field(..., description="CNPJ")
    telefone: Optional[str] = Field(None, description="Telefone")
    enderecos: EnderecoCreate = Field(..., description="Endereço do fornecedor")

class FornecedorUpdate(BaseModel):
    model_config = ConfigDict(extra="allow")
    nome: Optional[str] = Field(None, description="Nome do fornecedor")
    email: Optional[str] = Field(None, description="E-mail do fornecedor")
    cnpj: Optional[str] = Field(None, description="CNPJ")
    telefone: Optional[str] = Field(None, description="Telefone")
    enderecos: Optional[EnderecoCreate] = Field(None, description="Endereço do fornecedor")

class ProdutoCreate(BaseModel):
    model_config = ConfigDict(extra="allow")
    nome: str = Field(..., description="Nome do produto")
    descricao: Optional[str] = Field(None, description="Descrição")
    preco: Optional[float] = Field(None, ge=0, description="Preço")
    fornecedor_id: Optional[int] = Field(None, ge=1, description="ID do fornecedor")

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
    extra_params: dict | None = None,
    json_body: dict | None = None,
) -> Response:
    """
    Encaminha a requisição para o ms-fornecedores usando caminho RELATIVO
    à base configurada em settings.MS_FORNECEDORES_URL.
    """
    target_path = path.lstrip("/")
    method = request.method
    headers = dict(request.headers)
    params = dict(request.query_params)

    if extra_params:
        for k, v in extra_params.items():
            if v is not None:
                params[k] = v
            else:
                params.pop(k, None)

    headers.pop("host", None)
    headers.pop("content-length", None)
    headers.pop("transfer-encoding", None)

    try:
        async with httpx.AsyncClient(
            base_url=settings.MS_FORNECEDORES_URL, timeout=10.0
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
        raise HTTPException(status_code=504, detail="Timeout ao contactar serviço de fornecedores")
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail=f"Erro ao contactar serviço de fornecedores: {exc}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no gateway (fornecedores): {e}")

# =======================
#   ROTAS (ESPELHO ms-forncedores)
#   Base real do serviço: /api/v1/fornecedores
# =======================

@router.get("/", summary="Listar fornecedores")
async def listar_fornecedores_proxy(request: Request):
    """
    GET /api/v1/fornecedores/
    Lista todos os fornecedores.
    """
    return await _forward_request(request, "")

@router.post("/", summary="Criar fornecedor")
async def criar_fornecedor_proxy(
    request: Request,
    body: FornecedorCreate = Body(...),
):
    """
    POST /api/v1/fornecedores/
    Cria um fornecedor.
    """
    json_body = body.model_dump(exclude_none=True)
    return await _forward_request(request, "", json_body=json_body)

@router.get("/{fornecedor_id:int}", summary="Obter fornecedor por ID")
async def ler_fornecedor_proxy(
    request: Request,
    fornecedor_id: int = Path(..., ge=1, description="ID do fornecedor"),
):
    """
    GET /api/v1/fornecedores/{fornecedor_id}
    Obtém um fornecedor por ID.
    """
    return await _forward_request(request, f"{fornecedor_id}")

@router.put("/{id:int}", summary="Atualizar fornecedor")
async def atualizar_fornecedor_proxy(
    request: Request,
    id: int = Path(..., ge=1, description="ID do fornecedor"),
    body: FornecedorUpdate = Body(...),
):
    """
    PUT /api/v1/fornecedores/{id}
    Atualiza um fornecedor.
    """
    json_body = body.model_dump(exclude_none=True)
    return await _forward_request(request, f"{id}", json_body=json_body)

@router.delete("/{fornecedor_id:int}", summary="Deletar fornecedor")
async def deletar_fornecedor_proxy(
    request: Request,
    fornecedor_id: int = Path(..., ge=1, description="ID do fornecedor"),
):
    """
    DELETE /api/v1/fornecedores/{fornecedor_id}
    Deleta um fornecedor.
    """
    return await _forward_request(request, f"{fornecedor_id}")

@router.put("/endedereco/{id:int}", summary="Atualizar endereço do fornecedor")
async def atualizar_endereco_proxy(
    request: Request,
    id: int = Path(..., ge=1, description="ID do endereço"),
    body: EnderecoCreate = Body(...),
):
    """
    PUT /api/v1/fornecedores/endedereco/{id}
    Atualiza endereço de um fornecedor.
    """
    json_body = body.model_dump(exclude_none=True)
    return await _forward_request(request, f"endedereco/{id}", json_body=json_body)

# ---------- PRODUTOS VINCULADOS A FORNECEDOR ----------

@router.post("/produtos", summary="Criar produto")
async def criar_produto_proxy(
    request: Request,
    body: ProdutoCreate = Body(...),
):
    """
    POST /api/v1/fornecedores/produtos
    Cria um produto vinculado (no ms-forncedores).
    """
    json_body = body.model_dump(exclude_none=True)
    return await _forward_request(request, "produtos", json_body=json_body)

@router.get("/produtos/", summary="Listar produtos (filtro opcional)")
async def listar_produtos_proxy(
    request: Request,
    fornecedor_id: Optional[int] = Query(default=None, ge=1, description="Filtrar por fornecedor_id"),
    nome: Optional[str] = Query(default=None, description="Filtrar por nome"),
):
    """
    GET /api/v1/fornecedores/produtos/
    Lista produtos; pode filtrar por fornecedor_id e/ou nome.
    """
    extra_params = {"fornecedor_id": fornecedor_id, "nome": nome}
    return await _forward_request(request, "produtos/", extra_params=extra_params)

@router.put("/produtos/{produto_id:int}", summary="Atualizar produto")
async def atualizar_produto_proxy(
    request: Request,
    produto_id: int = Path(..., ge=1, description="ID do produto"),
    body: ProdutoCreate = Body(...),
):
    """
    PUT /api/v1/fornecedores/produtos/{produto_id}
    Atualiza um produto.
    """
    json_body = body.model_dump(exclude_none=True)
    return await _forward_request(request, f"produtos/{produto_id}", json_body=json_body)
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
from datetime import date
from pydantic import BaseModel, Field, ConfigDict

from ..core.config import settings

router = APIRouter()

# =======================
#   MODELOS P/ DOCS (espelho do schema atual)
# =======================

class EnderecoCreate(BaseModel):
    model_config = ConfigDict(extra="allow")
    funcionario_id: int = Field(..., description="ID do funcionário (obrigatório no schema atual)")
    logradouro: str = Field(..., description="Logradouro (rua/avenida)")
    numero: str = Field(..., description="Número")
    complemento: Optional[str] = Field(None, description="Complemento")
    bairro: str = Field(..., description="Bairro")
    cidade: str = Field(..., description="Cidade")
    estado: str = Field(..., description="UF")
    cep: str = Field(..., description="CEP")

class FuncionarioCreate(BaseModel):
    model_config = ConfigDict(extra="allow")
    nome: str = Field(..., description="Nome completo")
    cpf: str = Field(..., description="CPF")
    email: str = Field(..., description="E-mail")
    telefone: str = Field(..., description="Telefone")
    data_nascimento: date = Field(..., description="Data de nascimento (YYYY-MM-DD)")
    cargo: str = Field(..., description="Cargo")
    salario: float = Field(..., ge=0, description="Salário")
    senha: str = Field(..., description="Senha")
    data_contratacao: date = Field(..., description="Data de contratação (YYYY-MM-DD)")
    enderecos: EnderecoCreate = Field(..., description="Endereço do funcionário")

class EnderecoUpdate(EnderecoCreate):
    pass

class FuncionarioUpdate(BaseModel):
    model_config = ConfigDict(extra="allow")
    nome: Optional[str] = Field(None, description="Nome completo")
    email: Optional[str] = Field(None, description="E-mail")
    telefone: Optional[str] = Field(None, description="Telefone")
    cargo: Optional[str] = Field(None, description="Cargo")
    salario: Optional[float] = Field(None, ge=0, description="Salário")
    senha: Optional[str] = Field(None, description="Senha")

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
            base_url=settings.MS_FUNCIONARIOS_URL, timeout=10.0
        ) as client:
            if json_body is not None:
                r = await client.request(
                    method=method, url=target_path, headers=headers, params=params, json=json_body
                )
            else:
                content = await request.body()
                r = await client.request(
                    method=method, url=target_path, headers=headers, params=params, content=content
                )
        return _make_proxy_response(r)
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Timeout ao contactar serviço de funcionários")
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail=f"Erro ao contactar serviço de funcionários: {exc}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no gateway (funcionários): {e}")

# =======================
#   ROTAS (ESPELHO)
# =======================

@router.get("/", summary="Listar funcionários")
async def listar_funcionarios_proxy(
    request: Request,
    skip: int = Query(default=0, ge=0, description="Offset/paginação"),
    limit: int = Query(default=10, ge=1, le=1000, description="Tamanho da página"),
):
    extra_params = {"skip": skip, "limit": limit}
    return await _forward_request(request, "", extra_params=extra_params)

@router.post("/", summary="Criar funcionário")
async def criar_funcionario_proxy(
    request: Request,
    body: FuncionarioCreate = Body(...),
):
    # mode="json" -> converte date/datetime para string ISO
    json_body = body.model_dump(mode="json", exclude_none=True)
    return await _forward_request(request, "", json_body=json_body)

@router.put("/{id:int}", summary="Atualizar funcionário")
async def atualizar_funcionario_proxy(
    request: Request,
    id: int = Path(..., ge=1, description="ID do funcionário"),
    body: FuncionarioUpdate = Body(...),
):
    json_body = body.model_dump(mode="json", exclude_none=True)
    return await _forward_request(request, f"{id}", json_body=json_body)

@router.delete("/{id:int}", summary="Deletar funcionário")
async def deletar_funcionario_proxy(
    request: Request,
    id: int = Path(..., ge=1, description="ID do funcionário"),
):
    return await _forward_request(request, f"{id}")

@router.put("/endereco/{id:int}", summary="Atualizar endereço do funcionário")
async def atualizar_endereco_proxy(
    request: Request,
    id: int = Path(..., ge=1, description="ID do endereço"),
    body: EnderecoUpdate = Body(...),
):
    json_body = body.model_dump(mode="json", exclude_none=True)
    return await _forward_request(request, f"endereco/{id}", json_body=json_body)
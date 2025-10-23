import httpx
from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    Response,
    Query,
)
from datetime import date
from typing import Optional

from ..core.config import settings

router = APIRouter()

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
    Encaminha a requisição para o ms-relatorios usando caminho RELATIVO
    à base configurada em settings.MS_RELATORIOS_URL.
    """
    target_path = path.lstrip("/")
    method = request.method
    headers = dict(request.headers)
    params = dict(request.query_params)

    # inclui/normaliza query params explícitos (datas em ISO)
    if extra_params:
        for k, v in extra_params.items():
            if isinstance(v, date):
                params[k] = v.isoformat()
            elif v is not None:
                params[k] = v
            else:
                params.pop(k, None)

    headers.pop("host", None)
    headers.pop("content-length", None)
    headers.pop("transfer-encoding", None)

    try:
        async with httpx.AsyncClient(
            base_url=settings.MS_RELATORIOS_URL, timeout=15.0
        ) as client:
            if json_body is not None:
                r = await client.request(
                    method=method,
                    url=target_path,
                    headers=headers,
                    params=params,
                    json=json_body,  # se algum relatório aceitar POST com body
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
        raise HTTPException(status_code=504, detail="Timeout ao contactar serviço de relatórios")
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail=f"Erro ao contactar serviço de relatórios: {exc}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no gateway (relatórios): {e}")

# =======================
#   ROTAS (ESPELHO ms-relatorios)
#   Base real do serviço: /api/v1/relatorios
# =======================

@router.get("/vendas-sumario", summary="Relatório sumário de vendas")
async def gerar_relatorio_sumario_vendas_proxy(
    request: Request,
    data_inicio: Optional[date] = Query(default=None, description="Data inicial (YYYY-MM-DD)"),
    data_fim: Optional[date] = Query(default=None, description="Data final (YYYY-MM-DD)"),
):
    """
    GET /api/v1/relatorios/vendas-sumario
    Encaminha para o ms-relatorios gerando um sumário de vendas no período.
    """
    extra_params = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
    }
    return await _forward_request(request, "vendas-sumario", extra_params=extra_params)

@router.get("/vendas-por-periodo", summary="Vendas agregadas por período (dia/mês)")
async def vendas_por_periodo_proxy(
    request: Request,
    data_inicio: Optional[date] = Query(default=None, description="Data inicial (YYYY-MM-DD)"),
    data_fim: Optional[date] = Query(default=None, description="Data final (YYYY-MM-DD)"),
    granularidade: str = Query("dia", pattern="^(dia|mes)$", description="Agregação por 'dia' ou 'mes'")
):
    extra_params = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "granularidade": granularidade,
    }
    return await _forward_request(request, "vendas-por-periodo", extra_params=extra_params)



@router.get("/ranking-produtos", summary="Ranking de produtos (qtd/valor)")
async def ranking_produtos_proxy(
    request: Request,
    data_inicio: Optional[date] = Query(default=None, description="Data inicial (YYYY-MM-DD)"),
    data_fim: Optional[date] = Query(default=None, description="Data final (YYYY-MM-DD)"),
    ordenar_por: str = Query("valor", pattern="^(qtd|valor)$", description="Ordenar por 'qtd' ou 'valor'"),
    top: int = Query(10, ge=1, le=1000, description="Quantidade de itens no ranking"),
    incluir_titulos: bool = Query(False, description="Se true, enriquece com 'titulo' do ms-produtos")
):
    extra_params = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "ordenar_por": ordenar_por,
        "top": top,
        "incluir_titulos": incluir_titulos,
    }
    return await _forward_request(request, "ranking-produtos", extra_params=extra_params)



@router.get("/ranking-funcionarios", summary="Ranking de funcionários (qtd/valor)")
async def ranking_funcionarios_proxy(
    request: Request,
    data_inicio: Optional[date] = Query(default=None, description="Data inicial (YYYY-MM-DD)"),
    data_fim: Optional[date] = Query(default=None, description="Data final (YYYY-MM-DD)"),
    ordenar_por: str = Query("valor", pattern="^(qtd|valor)$", description="Ordenar por 'qtd' ou 'valor'"),
    top: int = Query(10, ge=1, le=1000, description="Quantidade de itens no ranking"),
    incluir_nomes: bool = Query(False, description="Se true, enriquece com 'nome' do ms-funcionarios")
):
    extra_params = {
        "data_inicio": data_inicio,
        "data_fim": data_fim,
        "ordenar_por": ordenar_por,
        "top": top,
        "incluir_nomes": incluir_nomes,
    }
    return await _forward_request(request, "ranking-funcionarios", extra_params=extra_params)
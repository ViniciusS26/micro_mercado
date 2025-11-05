import httpx
from datetime import date
from typing import Optional, Dict, Any, Literal, cast
from collections import defaultdict
from fastapi import HTTPException
from functools import lru_cache

from ..schemas import schemas_relatorios as schemas  # Importa os nossos schemas de relatório

# URL base da API do ms-vendas (deve apontar diretamente para o microserviço de vendas)
MS_VENDAS_URL = "http://172.31.23.32/api/v1/vendas/"
MS_PRODUTOS_URL = "http://172.31.21.142/api/v1/produtos/"
MS_FUNCIONARIOS_URL = "http://172.31.21.126/api/v1/funcionarios/"


# ============================================================
#  RELATÓRIO: SUMÁRIO DE VENDAS
# ============================================================
async def obter_sumario_vendas_periodo(
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None
) -> schemas.RelatorioVendasSumario:
    """
    Busca as estatísticas de vendas do ms-vendas para um determinado período.
    """
    params = {}
    if data_inicio:
        params["data_inicio"] = data_inicio.isoformat()
    if data_fim:
        params["data_fim"] = data_fim.isoformat()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(MS_VENDAS_URL, params=params)
            response.raise_for_status()
            data = response.json()

            if "estatisticas" not in data:
                raise HTTPException(status_code=500, detail="Resposta inválida do serviço de vendas (sem estatísticas)")

            stats = data["estatisticas"]

            relatorio = schemas.RelatorioVendasSumario(
                periodo_inicio=data_inicio,
                periodo_fim=data_fim,
                total_vendas=stats.get("total_registros", 0),
                valor_total_vendido=stats.get("valor_total_periodo", 0.0),
                total_produtos_vendidos=stats.get("total_produtos_periodo", 0)
            )
            return relatorio

        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Erro ao comunicar com o serviço de vendas: {exc}")
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=f"Serviço de vendas retornou erro: {exc.response.text}")
        except Exception as exc:
            raise HTTPException(status_code=500, detail=f"Erro inesperado ao processar dados de vendas: {exc}")


# ============================================================
#  RELATÓRIO: VENDAS POR PERÍODO (DIA / MÊS)
# ============================================================
async def obter_vendas_por_periodo(
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    granularidade: str = "dia",  # "dia" ou "mes"
) -> schemas.RelatorioVendasPorPeriodo:
    """
    Agrega vendas por dia ou mês consultando o ms-vendas.
    """
    if granularidade not in ("dia", "mes"):
        raise HTTPException(status_code=422, detail="granularidade deve ser 'dia' ou 'mes'")

    params: Dict[str, Any] = {}
    if data_inicio is not None:
        params["data_inicio"] = data_inicio.isoformat()
    if data_fim is not None:
        params["data_fim"] = data_fim.isoformat()
    params["limit"] = 1000
    params["skip"] = 0

    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(MS_VENDAS_URL, params=params)
            r.raise_for_status()
            page = r.json()
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail=f"Erro ao comunicar com ms-vendas: {exc}")
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=f"ms-vendas retornou erro: {exc.response.text}")

    # Extrai lista de vendas (ajuste para a sua chave real)
    items = page.get("vendas") or page.get("items") or page.get("results") or []

    # Agrupamento
    buckets: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"quantidade_vendas": 0, "valor_total": 0.0})
    for v in items:
        dt = v.get("data") or v.get("data_venda") or v.get("created_at") or ""
        if not isinstance(dt, str) or len(dt) < 10:
            continue

        key = dt[:7] if granularidade == "mes" else dt[:10]
        buckets[key]["quantidade_vendas"] += 1
        valor = v.get("valor_total") or v.get("total") or 0
        try:
            buckets[key]["valor_total"] += float(valor)
        except (TypeError, ValueError):
            pass

    # Monta lista de objetos Pydantic tipados (para evitar erro do mypy)
    series_objs = [
        schemas.VendasPeriodoItem(
            periodo=k,
            quantidade_vendas=v["quantidade_vendas"],
            valor_total=round(v["valor_total"], 2),
        )
        for k, v in sorted(buckets.items(), key=lambda kv: kv[0])
    ]

    # Granularidade como Literal["dia","mes"] para o mypy
    typed_granularidade: Literal["dia", "mes"] = cast(Literal["dia", "mes"], granularidade)

    return schemas.RelatorioVendasPorPeriodo(
        granularidade=typed_granularidade,
        series=series_objs,
    )
    


def _coalesce(*vals, default=None):
    for v in vals:
        if v is not None:
            return v
    return default

@lru_cache(maxsize=512)
def _buscar_titulo_produto(produto_id: int) -> str | None:
    try:
        # busca direta no ms-produtos
        r = httpx.get(f"{MS_PRODUTOS_URL}{produto_id}", timeout=5.0)
        if r.status_code == 200:
            j = r.json()
            # tenta achar 'titulo' ou 'nome'
            return _coalesce(j.get("titulo"), j.get("nome"))
    except Exception:
        pass
    return None

async def obter_ranking_produtos(
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    ordenar_por: str = "valor",  # 'qtd' ou 'valor'
    top: int = 10,
    incluir_titulos: bool = False,
) -> schemas.RelatorioRankingProdutos:
    """
    Soma quantidade e valor por produto no período e retorna o top-N.
    """
    if ordenar_por not in ("qtd", "valor"):
        raise HTTPException(status_code=422, detail="ordenar_por deve ser 'qtd' ou 'valor'")
    if top < 1 or top > 1000:
        raise HTTPException(status_code=422, detail="top deve estar entre 1 e 1000")

    # monta params para ms-vendas
    params: Dict[str, Any] = {}
    if data_inicio is not None:
        params["data_inicio"] = data_inicio.isoformat()
    if data_fim is not None:
        params["data_fim"] = data_fim.isoformat()
    params["limit"] = 1000
    params["skip"] = 0

    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(MS_VENDAS_URL, params=params)
            r.raise_for_status()
            page = r.json()
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail=f"Erro ao comunicar com ms-vendas: {exc}")
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=f"ms-vendas retornou erro: {exc.response.text}")

    vendas = page.get("vendas") or page.get("items") or page.get("results") or []

    # agrega por produto_id
    agg: Dict[int, Dict[str, Any]] = {}
    for v in vendas:
        itens = v.get("itens") or v.get("items") or []
        for it in itens:
            # tenta extrair o produto_id de várias chaves comuns
            produto_id = _coalesce(
                it.get("produto_id"),
                it.get("produtoId"),
                it.get("id_produto"),
                it.get("produto"),
            )
            if not isinstance(produto_id, int):
                # tenta converter se vier como str numérica
                try:
                    produto_id = int(produto_id)
                except Exception:
                    continue
            qtd = _coalesce(it.get("quantidade"), it.get("qtd"), it.get("qtde"), 1)
            try:
                qtd = int(qtd)
            except Exception:
                qtd = 1

            # tenta obter valor do item; se não vier, calcula qtd * preco_unitario
            valor_item = _coalesce(
                it.get("valor_total"),
                it.get("total"),
                it.get("preco_total"),
                it.get("subtotal"),
                it.get("valor"),
            )
            if valor_item is None:
                pu = _coalesce(it.get("preco_unitario"), it.get("preco"), it.get("unit_price"), 0)
                try:
                    valor_item = float(pu) * qtd
                except Exception:
                    valor_item = 0.0
            else:
                try:
                    valor_item = float(valor_item)
                except Exception:
                    valor_item = 0.0

            if produto_id not in agg:
                agg[produto_id] = {"qtd_total": 0, "valor_total": 0.0}
            agg[produto_id]["qtd_total"] += qtd
            agg[produto_id]["valor_total"] += valor_item

    # ordena conforme solicitado
    key = (lambda x: x[1]["qtd_total"]) if ordenar_por == "qtd" else (lambda x: x[1]["valor_total"])
    ordenado = sorted(agg.items(), key=key, reverse=True)[:top]

    itens_objs = []
    for pid, vals in ordenado:
        titulo = _buscar_titulo_produto(pid) if incluir_titulos else None
        itens_objs.append(
            schemas.RankingProdutoItem(
                produto_id=pid,
                titulo=titulo,
                qtd_total=int(vals["qtd_total"]),
                valor_total=round(float(vals["valor_total"]), 2),
            )
        )

    typed_ordenar: Literal["qtd", "valor"] = cast(Literal["qtd", "valor"], ordenar_por)
    return schemas.RelatorioRankingProdutos(
        ordenar_por=typed_ordenar,
        top=top,
        itens=itens_objs,
    )
    

@lru_cache(maxsize=512)
def _buscar_nome_funcionario(funcionario_id: int) -> str | None:
    try:
        r = httpx.get(f"{MS_FUNCIONARIOS_URL}{funcionario_id}", timeout=5.0)
        if r.status_code == 200:
            j = r.json()
            return j.get("nome") or j.get("name")
    except Exception:
        pass
    return None


async def obter_ranking_funcionarios(
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    ordenar_por: str = "valor",  # 'qtd' ou 'valor'
    top: int = 10,
    incluir_nomes: bool = False,
) -> schemas.RelatorioRankingFuncionarios:
    """
    Soma quantidade de vendas e valor por funcionário no período e retorna top-N.
    """
    if ordenar_por not in ("qtd", "valor"):
        raise HTTPException(status_code=422, detail="ordenar_por deve ser 'qtd' ou 'valor'")
    if top < 1 or top > 1000:
        raise HTTPException(status_code=422, detail="top deve estar entre 1 e 1000")

    # Params para ms-vendas
    params: Dict[str, Any] = {}
    if data_inicio is not None:
        params["data_inicio"] = data_inicio.isoformat()
    if data_fim is not None:
        params["data_fim"] = data_fim.isoformat()
    params["limit"] = 1000
    params["skip"] = 0

    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(MS_VENDAS_URL, params=params)
            r.raise_for_status()
            page = r.json()
    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail=f"Erro ao comunicar com ms-vendas: {exc}")
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=f"ms-vendas retornou erro: {exc.response.text}")

    vendas = page.get("vendas") or page.get("items") or page.get("results") or []

    # agrega por funcionario_id
    agg: Dict[int, Dict[str, Any]] = {}
    for v in vendas:
        funcionario_id = v.get("funcionario_id") or v.get("funcionarioId") or v.get("id_funcionario")
        if not isinstance(funcionario_id, int):
            try:
                funcionario_id = int(funcionario_id)
            except Exception:
                continue

        valor_total = v.get("valor_total") or v.get("total") or 0
        try:
            valor_total = float(valor_total)
        except Exception:
            valor_total = 0.0

        if funcionario_id not in agg:
            agg[funcionario_id] = {"qtd_vendas": 0, "valor_total": 0.0}
        agg[funcionario_id]["qtd_vendas"] += 1
        agg[funcionario_id]["valor_total"] += valor_total

    key = (lambda x: x[1]["qtd_vendas"]) if ordenar_por == "qtd" else (lambda x: x[1]["valor_total"])
    ordenado = sorted(agg.items(), key=key, reverse=True)[:top]

    itens_objs = []
    for fid, vals in ordenado:
        nome = _buscar_nome_funcionario(fid) if incluir_nomes else None
        itens_objs.append(
            schemas.RankingFuncionarioItem(
                funcionario_id=fid,
                nome=nome,
                qtd_vendas=int(vals["qtd_vendas"]),
                valor_total=round(float(vals["valor_total"]), 2),
            )
        )

    typed_ordenar: Literal["qtd", "valor"] = cast(Literal["qtd", "valor"], ordenar_por)
    return schemas.RelatorioRankingFuncionarios(
        ordenar_por=typed_ordenar,
        top=top,
        itens=itens_objs,
    )
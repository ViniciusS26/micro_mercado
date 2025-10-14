import httpx
from fastapi import FastAPI, Request, Response


app = FastAPI()

SERVICO_FUNCIONARIOS = "http://127.0.0.1:8001/"
SERVICO_PRODUTOS = "http://127.0.0.1:8002/"
SERVICO_VENDAS = "http://127.0.0.1:8003/"
SERVICO_FORNECEDORES = "http://127.0.0.1:8006/"
SERVICO_RELATORIOS = "http://127.0.0.1:8005/"


client = httpx.AsyncClient()

async def manda_requisicao_urls(request:Request, url:str):
    """
    Função para mandar requisições para os serviços

    Parameters
    ----------
        request : Request
            Requisição recebida pela API Gateway
        url : str
            URL do serviço para onde a requisição deve ser encaminhada
        Returns
        -------
        Response
            Resposta recebida do serviço

    """
    metodo = request.method
    headers = dict(request.headers)
    body = await request.body()

    try:
        #faz a requisição ao serviço apropriado
        resposta = await client.request(
            metodo, url, headers=headers, content=body, timeout=10.0
        )

        # Retorna a resposta do serviço original
        return Response(
            content=resposta.content,
            status_code=resposta.status_code,
            headers=resposta.headers
        )
    except httpx.RequestError as e:
        return Response(
            content=f"Erro ao conectar com o serviço: {e}",
            status_code=502
        )

@app.api_route("fornecedores/{caminho:path}", methods=["GET","POST","PUT","DELETE"])
async def fornecedores(request:Request,caminho:str):
    """Rota para encaminhar requisições relacionadas a fornecedores
    para o serviço de fornecedores."""
    url = f"{SERVICO_FORNECEDORES}/{caminho}"
    return await manda_requisicao_urls(request,url)

@app.api_route("/{caminho:path}", methods=["GET","POST","PUT","DELETE"])
async def produtos(request:Request,caminho:str):
    """Rota para encaminhar requisições relacionadas a produtos"""
    """para o serviço de produtos."""
    url = f"{SERVICO_PRODUTOS}/{caminho}"
    return await manda_requisicao_urls(request,url)

@app.api_route("/{caminho:path}", methods=["GET","POST","PUT","DELETE"])
async def vendas(request:Request,caminho:str):
    """Rota para encaminhar requisições relacionadas a vendas"""
    url = f"{SERVICO_VENDAS}/{caminho}"
    return await manda_requisicao_urls(request,url)

@app.api_route("/{caminho:path}", methods=["GET","POST","PUT","DELETE"])
async def fornecedores(request:Request,caminho:str):
    """Rota para encaminhar requisições relacionadas a fornecedores"""
    url = f"{SERVICO_FORNECEDORES}/{caminho}"
    return await manda_requisicao_urls(request,url)

@app.get("/info")
def info():
    return {"status": "API Gateway está funcionando!"}
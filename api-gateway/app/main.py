from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importa todos os routers que criamos
from .routers import (
    funcionarios_router,
    fornecedores_router,
    produtos_router,
    vendas_router,
    relatorios_router
)

app = FastAPI(
    title="API Gateway - Sistema SGM",
    description="Ponto de entrada único para os microsserviços do Sistema SGM.",
    version="1.0.0"
)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Ajustar em produção para o URL do frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui os routers na aplicação principal
# Cada include_router define o prefixo base para as rotas daquele microsserviço
# e uma tag para agrupar na documentação /docs
app.include_router(
    funcionarios_router.router, 
    prefix="/api/v1/funcionarios", 
    tags=["Funcionários"]
)
app.include_router(
    fornecedores_router.router, 
    prefix="/api/v1/fornecedores", 
    tags=["Fornecedores"]
)
app.include_router(
    produtos_router.router, 
    prefix="/api/v1/produtos", 
    tags=["Produtos"]
)
app.include_router(
    vendas_router.router, 
    prefix="/api/v1/vendas", 
    tags=["Vendas"]
)
app.include_router(
    relatorios_router.router, 
    prefix="/api/v1/relatorios", 
    tags=["Relatórios"]
)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "API Gateway do Sistema SGM está operacional!"}
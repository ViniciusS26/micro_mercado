from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importa o router dos endpoints
from .api import endpoints

# Importa a engine e a Base do SQLAlchemy (mesmo sem modelos agora, para consistência)
from .db.database import engine, Base

# Se tivéssemos modelos em models/models_relatorios.py, esta linha os criaria
# Base.metadata.create_all(bind=engine) 
# Por agora, podemos deixá-la comentada ou removê-la se não houver modelos.

app = FastAPI(
    title="Microsserviço de Relatórios",
    description="API para gerar relatórios agregados do sistema SGM.",
    version="1.0.0"
)

# Configuração do CORS (igual aos outros serviços)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ajustar em produção
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas definidas no router de endpoints
app.include_router(endpoints.router, prefix="/api/v1")

# (Opcional) Endpoint raiz para verificar se o serviço está no ar
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bem-vindo ao Microsserviço de Relatórios!"}
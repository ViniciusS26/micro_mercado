from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import endpoints
from .db.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API VENDAS - Sistema SGM",
    description="Ponto de entrada único para os microsserviços VENDAS.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restrinja para o domínio do seu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(endpoints.router, prefix="/api/v1")
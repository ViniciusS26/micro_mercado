import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import  routes_produtos
from .db.connection import engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API PRODUTOS - Sistema SGM",
    description="Ponto de entrada.",
    version="1.0.0"
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)


app.include_router(routes_produtos.router, prefix="/api/v1")
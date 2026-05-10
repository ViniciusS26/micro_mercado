import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import  routes_funcionario, routes_produtos, routes_vendas, routes_relatorio
from db.connection import engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API FUNCIONÁRIOS - Sistema SGM",
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


app.include_router(routes_funcionario.router, prefix="/api/v1")
app.include_router(routes_produtos.router, prefix="/api/v1")
app.include_router(routes_vendas.router, prefix="/api/v1")
app.include_router(routes_relatorio.router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)

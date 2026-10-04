import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from .routes import  routes_funcionario
from .db.connection import engine, Base


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API FUNCIONÁRIOS - Sistema SGM",
    description="Ponto de entrada.",
    version="1.0.0",
    docs_url="/api/v1/funcionarios/docs",
    openapi_url="/api/v1/funcionarios/openapi.json",
)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)


@app.get("/healthz", include_in_schema=False)
def healthz():
    return {"status": "alive"}


@app.get("/readyz", include_in_schema=False)
def readyz():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError:
        return JSONResponse(status_code=503, content={"status": "not_ready"})
    return {"status": "ready"}


app.include_router(routes_funcionario.router, prefix="/api/v1")
Instrumentator().instrument(app).expose(app, endpoint="/metrics", include_in_schema=False)


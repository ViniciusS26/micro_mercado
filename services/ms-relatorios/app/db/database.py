import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

NOVA_PORTA = "5432" # Porta definida para o PostgreSQL

# Define a URL do banco de dados para db_relatorios na porta 5435
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"postgresql://postgres:root@localhost:{NOVA_PORTA}/db_relatorios"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para os modelos SQLAlchemy (mesmo que não tenhamos modelos agora, é bom ter)
Base = declarative_base()
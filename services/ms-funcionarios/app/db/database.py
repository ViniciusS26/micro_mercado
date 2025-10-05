import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:vini123@db_funcionarios/funcionarios_db" # Valor padrão para DEV local
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# O aviso sobre 'orm_mode' para 'from_attributes' é do Pydantic V2 e não é fatal para o deploy.
# Resolva-o alterando orm_mode=True para from_attributes=True em seus modelos Pydantic.
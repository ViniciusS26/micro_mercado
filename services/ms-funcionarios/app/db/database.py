import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# -------------------------------------------------------------------
# IMPORTANTE: AQUI É A MUDANÇA!
# Obtém a URL do banco de dados da variável de ambiente.
# Se a variável de ambiente não estiver definida, usa a URL local como padrão
# para desenvolvimento (mas certifique-se de que isso é o que você quer).
#
# A string "postgresql://postgres:vini123@database:5432/db_associates"
# é para uso LOCAL com docker-compose.
#
# A string do Render é configurada APENAS no painel do Render.
# -------------------------------------------------------------------
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:vini123@database:5432/db_funcionarios" # Valor padrão para DEV local
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# O aviso sobre 'orm_mode' para 'from_attributes' é do Pydantic V2 e não é fatal para o deploy.
# Resolva-o alterando orm_mode=True para from_attributes=True em seus modelos Pydantic.
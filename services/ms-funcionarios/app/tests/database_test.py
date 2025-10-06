from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from  ..db.database import Base

# URL para o seu banco de dados DE TESTE. Pode ser um SQLite em memória ou outro DB.
# Usar um DB de teste no PostgreSQL é o ideal para manter a paridade com produção.
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:vini123@db_funcionarios/funcionarios_db_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Função para criar e limpar as tabelas do banco a cada sessão de teste
def setup_database():
    # Apaga e recria todas as tabelas. Garante um ambiente limpo.
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from  ..db.database import Base


SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost:5432/db_funcionarios"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def setup_database():
   
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

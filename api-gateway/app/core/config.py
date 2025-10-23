import os

class Settings:
    MS_FUNCIONARIOS_URL: str = os.getenv("MS_FUNCIONARIOS_URL", "http://localhost:8001/api/v1/funcionarios")
    MS_FORNECEDORES_URL: str = os.getenv("MS_FORNECEDORES_URL", "http://localhost:8050/api/v1/fornecedores")
    MS_PRODUTOS_URL: str = os.getenv("MS_PRODUTOS_URL", "http://localhost:8002/api/v1/produtos")
    MS_VENDAS_URL: str = os.getenv("MS_VENDAS_URL", "http://localhost:8004/api/v1/vendas")
    MS_RELATORIOS_URL: str = os.getenv("MS_RELATORIOS_URL", "http://localhost:8003/api/v1/relatorios")

settings = Settings()
import os

class Settings:
    MS_FUNCIONARIOS_URL: str = os.getenv("MS_FUNCIONARIOS_URL", "http://ms_funcionarios:8001/api/v1/funcionarios")
    MS_PRODUTOS_URL: str = os.getenv("MS_PRODUTOS_URL", "http://ms_produtos:8002/api/v1/produtos")
    MS_VENDAS_URL: str = os.getenv("MS_VENDAS_URL", "http://ms_vendas:8004/api/v1/vendas")
    MS_RELATORIOS_URL: str = os.getenv("MS_RELATORIOS_URL", "http://ms_relatorios:8003/api/v1/relatorios")

settings = Settings()
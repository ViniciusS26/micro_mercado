import os

class Settings:
    MS_FUNCIONARIOS_URL: str = os.getenv("MS_FUNCIONARIOS_URL", "http://172.31.21.126/api/v1/funcionarios")
    MS_PRODUTOS_URL: str = os.getenv("MS_PRODUTOS_URL", "http://172.31.21.142/api/v1/produtos/")
    MS_VENDAS_URL: str = os.getenv("MS_VENDAS_URL", "http://172.31.23.32/api/v1/vendas")
    MS_RELATORIOS_URL: str = os.getenv("MS_RELATORIOS_URL", "http://172.31.20.8/api/v1/relatorios")

settings = Settings()
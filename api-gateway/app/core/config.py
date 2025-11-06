import os

class Settings:
    MS_FUNCIONARIOS_URL: str = os.getenv("MS_FUNCIONARIOS_URL", "http://54.235.39.176/api/v1/funcionarios")
    MS_PRODUTOS_URL: str = os.getenv("MS_PRODUTOS_URL", "http://34.234.88.237/api/v1/produtos/")
    MS_VENDAS_URL: str = os.getenv("MS_VENDAS_URL", "http://3.91.44.244/api/v1/vendas")
    MS_RELATORIOS_URL: str = os.getenv("MS_RELATORIOS_URL", "http:/52.91.185.99/api/v1/relatorios")

settings = Settings()
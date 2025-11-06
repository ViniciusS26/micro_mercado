import os

class Settings:
    MS_FUNCIONARIOS_URL: str = os.getenv("MS_FUNCIONARIOS_URL", "http://54.235.39.176/api/v1/funcionarios")
    MS_PRODUTOS_URL: str = os.getenv("MS_PRODUTOS_URL", "http://54.159.92.230/api/v1/produtos")
    MS_VENDAS_URL: str = os.getenv("MS_VENDAS_URL", "http://34.228.197.814/api/v1/vendas")
    MS_RELATORIOS_URL: str = os.getenv("MS_RELATORIOS_URL", "http://18.208.246.140/api/v1/relatorios")

settings = Settings()
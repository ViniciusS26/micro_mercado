from zoneinfo import ZoneInfo
from pwdlib import PasswordHash
from datetime import datetime, timedelta
from datetime import datetime, timedelta, timezone
from jose import JWTError
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException, status
from http import HTTPStatus
from jwt import encode, decode, DecodeError
from fastapi.security import OAuth2PasswordBearer
from http import HTTPStatus
from pydantic import BaseModel, ConfigDict
from db.dependeces import get_db  as get_session


import os
from dotenv import load_dotenv

from models.models_funcionarios import Funcionarios

load_dotenv()

SECRETY_KEY = os.getenv("SECRETY_KEY", "FSDFSDFSDFSDFSDSDS.ASDASDASDASD")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))  # 7 dias

class FuncionarioTokken(BaseModel):
    id: int
    nome: str
    cpf: str
    cargo: str

    model_config = ConfigDict(from_attributes=True)



pwd_context = PasswordHash.recommended()


auth2_scheme = OAuth2PasswordBearer(tokenUrl="funcionarios/auth/")

def get_password_hash(password: str):
    """Retorna o hash da senha do usuário.
    Args:
        password (str): senha do usuário.
    Returns:
        str: hash da senha.
    """
    return pwd_context.hash(password)



def verify_password(plain_password: str, hashed_password: str):
    """Verifica se a senha informada é igual ao hash da senha.
    Args:
        plain_password (str): senha informada.
        hashed_password (str): hash da senha.
    Returns:
        bool: True se a senha for igual ao hash da senha, False caso contrário.
    """
    return pwd_context.verify(plain_password, hashed_password)



def create_access_token(data_payload: dict):
    """Cria um token de acesso para o usuário.
    Args:
        data_payload (dict): dados do usuário a serem incluídos no token.
    Returns:
        str: token de acesso.
    """
    # Define o tempo de expiração do token
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Cria o token
    token = encode(
        {"exp": expire, **data_payload},
        SECRETY_KEY,
        algorithm=ALGORITHM
    )
    return token


def verify_access_token(token: str, credentials_exception):
    """Verifica se o token de acesso é válido.
    Args:
        token (str): token de acesso.
        credentials_exception: exceção a ser levantada em caso de falha na verificação.
    Returns:
        TokenData: dados do usuário extraídos do token.
    """
    try:
        payload = decode(token, SECRETY_KEY, algorithms=[ALGORITHM])
        cpf: str = payload.get("sub")
        if cpf is None:
            raise credentials_exception
        token_data = FuncionarioTokken(cpf=cpf)
    except (JWTError, DecodeError):
        raise credentials_exception
    return token_data


def authenticate_user(db: Session, cpf: str, password: str):
    """Autentica o usuário verificando CPF e Senha."""
    
    # 1. Busca o funcionário pelo CPF na tabela Funcionarios
    funcionario = db.query(Funcionarios).filter(Funcionarios.cpf == cpf).first()
    
    # 2. Verifica se o funcionário existe e se a senha está correta
    if not funcionario or not verify_password(password, funcionario.senha):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="CPF ou senha inválidos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return funcionario
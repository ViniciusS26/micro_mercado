from zoneinfo import ZoneInfo
from pwdlib import PasswordHash
from datetime import datetime, timedelta
from datetime import datetime, timedelta, timezone
from jwt import encode
from jose import JWTError
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from fastapi import Depends,HTTPException, status
from http import HTTPStatus
from jwt import encode, decode, DecodeError
from fastapi.security import OAuth2PasswordBearer
from http import HTTPStatus
from pydantic import BaseModel, ConfigDict
from ..core.config import settings
from ..db.connection import get_db  as get_session



class FuncionarioTokken(BaseModel):
    id: int
    nome: str
    cpf: str
    cargo: str

    model_config = ConfigDict(from_attributes=True)



pwd_context = PasswordHash.recommended()


auth2_scheme = OAuth2PasswordBearer(tokenUrl="funcionarios/auth")

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
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    # Cria o token
    token = encode(
        {"exp": expire, **data_payload},
        settings.SECRETY_KEY,
        algorithm=settings.ALGORITHM
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
        payload = decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        cpf: str = payload.get("sub")
        if cpf is None:
            raise credentials_exception
        token_data = FuncionarioTokken(cpf=cpf)
    except (JWTError, DecodeError):
        raise credentials_exception
    return token_data


def authenticate_user(db: Session = Depends(get_session), cpf:str = str, password:str = str):
    """Autentica o usuário a partir do token de acesso.
    Args:
        token (str): token de acesso.
        db (Session): sessão do banco de dados.
    Returns:
        Funcionarios: usuário autenticado.
    """
    funcionario_cpf = db.query(cpf).filter(cpf == cpf).first()
    if not funcionario_cpf or not verify_password(password, funcionario_cpf.senha):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return funcionario_cpf
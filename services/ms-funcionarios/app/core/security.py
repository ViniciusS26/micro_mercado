from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()



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
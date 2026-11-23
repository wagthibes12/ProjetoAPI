
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta

from config.config import settings
import jwt


# =========================
# CONFIGURAÇÃO DE SENHAS
# =========================

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


# =========================
# CRIAR HASH DA SENHA
# =========================

def cria_hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)


# =========================
# VERIFICAR SENHA
# =========================

def verifica_senha(
    senha_informada: str,
    senha_banco: str
) -> bool:
    try:
        return pwd_context.verify(
            senha_informada,
            senha_banco
        )

    except (ValueError, TypeError):
        return False


# =========================
# CRIAR TOKEN JWT
# =========================

def criar_token(info: str, role: str) -> str:

    vence_em = datetime.now(timezone.utc) + timedelta(
        minutes=settings.JWT_ACCESS_EXPIRE_MINUTES
    )

    payload = {
        "sub": info,
        "role": role,
        "exp": vence_em,
        "iss": settings.JWT_ISSUER
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )

    return token


# =========================
# DECODIFICAR TOKEN JWT
# =========================

def decodifica_token(token: str) -> dict:

    payload = jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
        issuer=settings.JWT_ISSUER,
        options={
            "require": ["exp", "iss", "sub"]
        }
    )

    # Verifica se o token possui identificação válida.
    identificador = payload.get("sub")

    if not isinstance(identificador, str) or not identificador.strip():
        raise jwt.InvalidTokenError(
            "Token sem identificação válida."
        )

    return payload

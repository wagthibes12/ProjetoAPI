
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from config.config import settings
import jwt


pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)



def cria_hash_senha(senha: str) -> str:
    return pwd_context.hash(senha)



def verifica_senha(
    senha_informada: str,
    senha_banco: str
) -> bool:
    try:
        return pwd_context.verify(senha_informada, senha_banco)
    except (ValueError, TypeError):
        return False



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

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )


def decodifica_token(token: str) -> dict:
    payload = jwt.decode(
        token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
        issuer=settings.JWT_ISSUER
    )

    return payload
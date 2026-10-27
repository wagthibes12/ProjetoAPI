
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
import jwt

from dependencies.dependencies import database
from entidades.models import Usuario, Perfil, UsuarioLogado
from core.security import decodifica_token


auth_scheme = HTTPBearer(auto_error=True)


def buscar_usuario_atual(
    credenciais: HTTPAuthorizationCredentials = Depends(auth_scheme),
    db: Session = Depends(database.get_db)
):
    try:
        payload = decodifica_token(credenciais.credentials)

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sessão expirada.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    identificador = payload.get("sub")

    if identificador is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token sem identificação do usuário.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    try:
        usuario_id = int(identificador)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identificação de usuário inválida.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    usuario = db.get(Usuario, usuario_id)

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado.",
            headers={"WWW-Authenticate": "Bearer"}
        )

    perfil = db.get(Perfil, usuario.perfil_id)

    if perfil is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="O usuário não possui um perfil válido."
        )

    return UsuarioLogado(
        id=usuario.id_usuario,
        nome=usuario.nome_completo,
        email=usuario.email,
        role=perfil.rotulo
    )


def verifica_permissao(*perfis_permitidos: str):
    def verificar(
        usuario: UsuarioLogado = Depends(buscar_usuario_atual)
    ):
        if usuario.role not in perfis_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para acessar este recurso."
            )

        return usuario

    return verificar

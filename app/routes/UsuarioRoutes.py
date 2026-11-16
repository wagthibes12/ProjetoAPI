
from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel import Session

from entidades.models import (
    UsuarioCriacao,
    UsuarioAtualizacao,
    UsuarioResposta,
)
from dependencies.dependencies import database
from dependencies.auth import verifica_permissao
from controllers import UsuarioController


usuario_router = APIRouter()


@usuario_router.get(
    "/usuarios",
    response_model=list[UsuarioResposta],
    status_code=status.HTTP_200_OK
)
def listar_usuarios(
    db: Session = Depends(database.get_db),
    usuario_atual=Depends(verifica_permissao("ADMIN"))
):
    try:
        usuarios = UsuarioController.buscar_todos_os_usuarios(db)
        return usuarios if usuarios else []

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@usuario_router.post(
    "/usuarios",
    response_model=UsuarioResposta,
    status_code=status.HTTP_201_CREATED
)
def inserir_usuario(
    usuario: UsuarioCriacao,
    db: Session = Depends(database.get_db),
    usuario_atual=Depends(verifica_permissao("ADMIN"))
):
    try:
        return UsuarioController.inserir_usuario(usuario, db)

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@usuario_router.put(
    "/usuarios/{usuario_id}",
    response_model=UsuarioResposta,
    status_code=status.HTTP_200_OK
)
def atualizar_usuario(
    usuario_id: int,
    usuario_data: UsuarioAtualizacao,
    db: Session = Depends(database.get_db),
    usuario_atual=Depends(verifica_permissao("ADMIN"))
):
    try:
        return UsuarioController.atualizar_usuario(
            db,
            usuario_id,
            usuario_data
        )

    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@usuario_router.delete(
    "/usuarios/{usuario_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def deletar_usuario(
    usuario_id: int,
    db: Session = Depends(database.get_db),
    usuario_atual=Depends(verifica_permissao("ADMIN"))
):
    try:
        UsuarioController.deletar_usuario(db, usuario_id)

    except KeyError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

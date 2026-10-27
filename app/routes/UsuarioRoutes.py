
from fastapi import APIRouter, Depends, status, HTTPException
from entidades.models import Usuario
from sqlmodel import Session
from dependencies.dependencies import database
from dependencies.auth import verifica_permissao
from controllers import UsuarioController


usuario_router = APIRouter()


@usuario_router.get(
    "/usuarios",
    response_model=list[Usuario],
    status_code=status.HTTP_200_OK
)
def listarusuarios(
    db: Session = Depends(database.get_db),
    usuario_atual=Depends(verifica_permissao("ADMIN"))
):
    try:
        usuario = UsuarioController.buscar_todos_os_usuarios(db)
        if not usuario:
            return []
        return usuario
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@usuario_router.post(
    "/usuarios",
    status_code=status.HTTP_201_CREATED,
    response_model=Usuario
)
def inserir_usuario(
    usuario: Usuario,
    db: Session = Depends(database.get_db),
    usuario_atual=Depends(verifica_permissao("ADMIN"))
):
    try:
        usuario_cadastrado = UsuarioController.inserir_usuario(usuario, db)
        return usuario_cadastrado
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@usuario_router.put(
    "/usuario/{usuario_id}",
    status_code=status.HTTP_200_OK
)
def atualizar_usuario(
    usuario_id: int,
    usuario_data: Usuario,
    db: Session = Depends(database.get_db),
    usuario_atual=Depends(verifica_permissao("ADMIN"))
):
    try:
        return UsuarioController.atualizar_usuario(
            db, usuario_id, usuario_data
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
def usuario_perfil(
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

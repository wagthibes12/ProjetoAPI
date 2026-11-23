
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from dependencies.dependencies import database
from dependencies.auth import (
    buscar_usuario_atual,
    verifica_permissao
)

from entidades.models import (
    UsuarioLogado,
    EmprestimoResposta
)

from controllers import EmprestimoController


router = APIRouter(
    prefix="/emprestimos",
    tags=["Empréstimos"]
)


# =========================
# REGISTRAR RETIRADA
# =========================

@router.post(
    "/solicitacao/{solicitacao_id}",
    response_model=EmprestimoResposta,
    status_code=status.HTTP_201_CREATED
)
def registrar_retirada(
    solicitacao_id: int,
    db: Session = Depends(database.get_db),
    usuario: UsuarioLogado = Depends(
        verifica_permissao("ADMIN", "GESTOR")
    )
):
    try:
        return EmprestimoController.registrar_retirada(
            db,
            solicitacao_id,
            usuario.id
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


# =========================
# LISTAR TODOS OS EMPRÉSTIMOS
# =========================

@router.get(
    "/",
    response_model=list[EmprestimoResposta]
)
def listar_todos(
    db: Session = Depends(database.get_db),
    usuario: UsuarioLogado = Depends(
        verifica_permissao("ADMIN", "GESTOR")
    )
):
    try:
        return EmprestimoController.listar_emprestimos(db)

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# =========================
# LISTAR EMPRÉSTIMOS ATIVOS
# =========================

@router.get(
    "/ativos",
    response_model=list[EmprestimoResposta]
)
def listar_ativos(
    db: Session = Depends(database.get_db),
    usuario: UsuarioLogado = Depends(
        verifica_permissao("ADMIN", "GESTOR")
    )
):
    try:
        return EmprestimoController.listar_emprestimos_ativos(db)

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# =========================
# LISTAR EMPRÉSTIMOS DO USUÁRIO
# =========================

@router.get(
    "/meus",
    response_model=list[EmprestimoResposta]
)
def listar_meus(
    db: Session = Depends(database.get_db),
    usuario: UsuarioLogado = Depends(buscar_usuario_atual)
):
    try:
        if usuario.role not in ("ADMIN", "GESTOR", "DISCENTE"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para acessar este recurso."
            )

        return EmprestimoController.listar_emprestimos_usuario(
            db,
            usuario.id
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# =========================
# CONSULTAR EMPRÉSTIMO POR ID
# =========================

@router.get(
    "/{emprestimo_id}",
    response_model=EmprestimoResposta
)
def consultar(
    emprestimo_id: int,
    db: Session = Depends(database.get_db),
    usuario: UsuarioLogado = Depends(buscar_usuario_atual)
):
    try:
        if usuario.role not in ("ADMIN", "GESTOR", "DISCENTE"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para acessar este recurso."
            )

        emprestimo = EmprestimoController.buscar_emprestimo(
            db,
            emprestimo_id
        )

        if usuario.role == "DISCENTE":
            pertence = EmprestimoController.verificar_proprietario(
                db,
                emprestimo_id,
                usuario.id
            )

            if not pertence:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Você não pode consultar o empréstimo de outro usuário."
                )

        return emprestimo

    except HTTPException:
        raise

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from dependencies.dependencies import database
from dependencies.auth import verifica_permissao

from entidades.models import (
    UsuarioLogado,
    DevolucaoCriacao,
    DevolucaoResposta
)

from controllers import DevolucaoController


router = APIRouter(
    prefix="/devolucoes",
    tags=["Devoluções"]
)


# =========================
# REGISTRAR DEVOLUÇÃO
# =========================

@router.post(
    "/emprestimo/{emprestimo_id}",
    response_model=DevolucaoResposta,
    status_code=status.HTTP_201_CREATED
)
def registrar(
    emprestimo_id: int,
    dados: DevolucaoCriacao,
    db: Session = Depends(database.get_db),
    usuario: UsuarioLogado = Depends(
        verifica_permissao("ADMIN", "GESTOR")
    )
):
    try:
        return DevolucaoController.registrar_devolucao(
            db,
            emprestimo_id,
            dados,
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
# LISTAR TODAS AS DEVOLUÇÕES
# =========================

@router.get(
    "/",
    response_model=list[DevolucaoResposta]
)
def listar(
    db: Session = Depends(database.get_db),
    usuario: UsuarioLogado = Depends(
        verifica_permissao("ADMIN", "GESTOR")
    )
):
    try:
        return DevolucaoController.listar_devolucoes(db)

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# =========================
# CONSULTAR DEVOLUÇÃO POR ID
# =========================

@router.get(
    "/{devolucao_id}",
    response_model=DevolucaoResposta
)
def consultar(
    devolucao_id: int,
    db: Session = Depends(database.get_db),
    usuario: UsuarioLogado = Depends(
        verifica_permissao("ADMIN", "GESTOR")
    )
):
    try:
        return DevolucaoController.buscar_devolucao(
            db,
            devolucao_id
        )

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

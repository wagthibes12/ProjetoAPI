
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from dependencies.dependencies import database
from dependencies.auth import (
    buscar_usuario_atual,
    verifica_permissao
)

from entidades.models import (
    UsuarioLogado,
    SolicitacaoCriacao,
    SolicitacaoResposta,
    SolicitacaoStatus
)

from controllers import SolicitacaoController


router = APIRouter(
    prefix="/solicitacoes",
    tags=["Solicitações"]
)


# =========================
# CRIAR SOLICITAÇÃO
# =========================

@router.post(
    "/",
    response_model=SolicitacaoResposta,
    status_code=status.HTTP_201_CREATED
)
def criar(
    dados: SolicitacaoCriacao,
    db: Session = Depends(database.get_db),
    usuario: UsuarioLogado = Depends(
        verifica_permissao("DISCENTE")
    )
):
    try:
        return SolicitacaoController.criar_solicitacao(
            db,
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
# LISTAR TODAS SOLICITAÇÕES
# ADMIN E GESTOR
# =========================

@router.get(
    "/",
    response_model=list[SolicitacaoResposta]
)
def listar_todas(
    db: Session = Depends(database.get_db),
    usuario: UsuarioLogado = Depends(
        verifica_permissao("ADMIN", "GESTOR")
    )
):
    try:
        return SolicitacaoController.listar_solicitacoes(db)

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# =========================
# LISTAR SOLICITAÇÕES DO DISCENTE
# =========================

@router.get(
    "/minhas",
    response_model=list[SolicitacaoResposta]
)
def listar_minhas(
    db: Session = Depends(database.get_db),
    usuario: UsuarioLogado = Depends(buscar_usuario_atual)
):
    try:
        if usuario.role == "DISCENTE":
            return SolicitacaoController.listar_solicitacoes_usuario(
                db,
                usuario.id
            )

        if usuario.role in ("ADMIN", "GESTOR"):
            return SolicitacaoController.listar_solicitacoes(db)

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar este recurso."
        )

    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


# =========================
# CONSULTAR SOLICITAÇÃO POR ID
# =========================

@router.get(
    "/{solicitacao_id}",
    response_model=SolicitacaoResposta
)
def consultar(
    solicitacao_id: int,
    db: Session = Depends(database.get_db),
    usuario: UsuarioLogado = Depends(buscar_usuario_atual)
):
    try:
        solicitacao = SolicitacaoController.buscar_solicitacao(
            db,
            solicitacao_id
        )

        if (
            usuario.role == "DISCENTE"
            and solicitacao.usuario_id != usuario.id
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não pode consultar a solicitação de outro usuário."
            )

        if usuario.role not in ("ADMIN", "GESTOR", "DISCENTE"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Você não tem permissão para acessar este recurso."
            )

        return solicitacao

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


# =========================
# APROVAR OU REJEITAR
# ADMIN E GESTOR
# =========================

@router.patch(
    "/{solicitacao_id}/status",
    response_model=SolicitacaoResposta
)
def analisar(
    solicitacao_id: int,
    novo_status: SolicitacaoStatus,
    db: Session = Depends(database.get_db),
    usuario: UsuarioLogado = Depends(
        verifica_permissao("ADMIN", "GESTOR")
    )
):
    try:
        return SolicitacaoController.atualizar_status_solicitacao(
            db,
            solicitacao_id,
            novo_status,
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
# CANCELAR SOLICITAÇÃO
# DISCENTE
# =========================

@router.patch(
    "/{solicitacao_id}/cancelar",
    response_model=SolicitacaoResposta
)
def cancelar(
    solicitacao_id: int,
    db: Session = Depends(database.get_db),
    usuario: UsuarioLogado = Depends(
        verifica_permissao("DISCENTE")
    )
):
    try:
        return SolicitacaoController.cancelar_solicitacao(
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

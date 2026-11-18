
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError, OperationalError
from datetime import datetime

from entidades.models import (
    Solicitacao,
    SolicitacaoCriacao,
    SolicitacaoStatus,
    Equipamento,
    EquipamentoStatus
)


# =========================
# CADASTRAR SOLICITAÇÃO
# =========================

def criar_solicitacao(
    db: Session,
    dados: SolicitacaoCriacao,
    usuario_id: int
):
    try:
        # Bloqueia temporariamente o equipamento.
        # Evita que duas solicitações sejam processadas
        # simultaneamente para o mesmo equipamento.
        statement = (
            select(Equipamento)
            .where(
                Equipamento.equipamento_id == dados.equipamento_id
            )
            .with_for_update()
        )

        equipamento = db.exec(statement).first()

        if equipamento is None:
            raise ValueError("Equipamento não encontrado.")

        # Verifica se o equipamento está disponível.
        if (
            equipamento.equipamento_status_equipamento
            != EquipamentoStatus.Disponivel
        ):
            raise ValueError(
                "Este equipamento não está disponível para solicitação."
            )

        # Verifica se já existe uma solicitação pendente
        # para o mesmo equipamento.
        solicitacao_pendente = db.exec(
            select(Solicitacao).where(
                Solicitacao.equipamento_id == dados.equipamento_id,
                Solicitacao.status_solicitacao
                == SolicitacaoStatus.Pendente
            ).with_for_update()
        ).first()

        if solicitacao_pendente is not None:
            raise ValueError(
                "Este equipamento já possui uma solicitação pendente."
            )

        # Valida as datas.
        if (
            dados.data_prevista_devolucao
            <= dados.data_prevista_retirada
        ):
            raise ValueError(
                "A data prevista de devolução deve ser posterior à retirada."
            )

        # Cria a solicitação.
        solicitacao = Solicitacao(
            usuario_id=usuario_id,
            equipamento_id=dados.equipamento_id,
            data_prevista_retirada=dados.data_prevista_retirada,
            data_prevista_devolucao=dados.data_prevista_devolucao,
            observacao=dados.observacao,
            status_solicitacao=SolicitacaoStatus.Pendente,
            data_solicitacao=datetime.now()
        )

        db.add(solicitacao)
        db.commit()
        db.refresh(solicitacao)

        return solicitacao

    except ValueError:
        db.rollback()
        raise

    except (IntegrityError, OperationalError) as e:
        db.rollback()
        raise RuntimeError(
            "Erro ao cadastrar solicitação no banco de dados."
        ) from e


# =========================
# LISTAR TODAS SOLICITAÇÕES
# =========================

def listar_solicitacoes(db: Session):
    try:
        statement = select(Solicitacao).order_by(
            Solicitacao.solicitacao_id.desc()
        )

        return db.exec(statement).all()

    except OperationalError as e:
        raise RuntimeError(
            "Erro ao consultar as solicitações."
        ) from e


# =========================
# CONSULTAR SOLICITAÇÃO POR ID
# =========================

def buscar_solicitacao(
    db: Session,
    solicitacao_id: int
):
    try:
        solicitacao = db.get(
            Solicitacao,
            solicitacao_id
        )

        if solicitacao is None:
            raise ValueError("Solicitação não encontrada.")

        return solicitacao

    except OperationalError as e:
        raise RuntimeError(
            "Erro ao consultar a solicitação."
        ) from e


# =========================
# LISTAR SOLICITAÇÕES DO USUÁRIO
# =========================

def listar_solicitacoes_usuario(
    db: Session,
    usuario_id: int
):
    try:
        statement = (
            select(Solicitacao)
            .where(Solicitacao.usuario_id == usuario_id)
            .order_by(Solicitacao.solicitacao_id.desc())
        )

        return db.exec(statement).all()

    except OperationalError as e:
        raise RuntimeError(
            "Erro ao consultar as solicitações do usuário."
        ) from e


# =========================
# ATUALIZAR STATUS
# =========================

def atualizar_status_solicitacao(
    db: Session,
    solicitacao_id: int,
    novo_status: SolicitacaoStatus,
    responsavel_id: int
):
    try:
        solicitacao = db.get(
            Solicitacao,
            solicitacao_id
        )

        if solicitacao is None:
            raise ValueError("Solicitação não encontrada.")

        if (
            solicitacao.status_solicitacao
            != SolicitacaoStatus.Pendente
        ):
            raise ValueError(
                "Somente solicitações pendentes podem ser analisadas."
            )

        if novo_status not in (
            SolicitacaoStatus.Aprovada,
            SolicitacaoStatus.Rejeitada
        ):
            raise ValueError(
                "Status inválido para análise da solicitação."
            )

        solicitacao.status_solicitacao = novo_status
        solicitacao.responsavel_id = responsavel_id
        solicitacao.data_analise = datetime.now()

        db.add(solicitacao)
        db.commit()
        db.refresh(solicitacao)

        return solicitacao

    except ValueError:
        db.rollback()
        raise

    except (IntegrityError, OperationalError) as e:
        db.rollback()
        raise RuntimeError(
            "Erro ao atualizar o status da solicitação."
        ) from e


# =========================
# CANCELAR SOLICITAÇÃO
# =========================

def cancelar_solicitacao(
    db: Session,
    solicitacao_id: int,
    usuario_id: int
):
    try:
        solicitacao = db.get(
            Solicitacao,
            solicitacao_id
        )

        if solicitacao is None:
            raise ValueError("Solicitação não encontrada.")

        if solicitacao.usuario_id != usuario_id:
            raise ValueError(
                "Você não pode cancelar uma solicitação de outro usuário."
            )

        if (
            solicitacao.status_solicitacao
            != SolicitacaoStatus.Pendente
        ):
            raise ValueError(
                "Somente solicitações pendentes podem ser canceladas."
            )

        solicitacao.status_solicitacao = SolicitacaoStatus.Cancelada

        db.add(solicitacao)
        db.commit()
        db.refresh(solicitacao)

        return solicitacao

    except ValueError:
        db.rollback()
        raise

    except (IntegrityError, OperationalError) as e:
        db.rollback()
        raise RuntimeError(
            "Erro ao cancelar a solicitação."
        ) from e

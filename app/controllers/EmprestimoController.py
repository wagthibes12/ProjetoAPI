
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError

from entidades.models import (
    Emprestimo,
    EmprestimoStatus,
    Solicitacao,
    SolicitacaoStatus,
    Equipamento,
    EquipamentoStatus
)


# =========================
# REGISTRAR RETIRADA
# =========================

def registrar_retirada(
    db: Session,
    solicitacao_id: int,
    responsavel_id: int
):
    try:
        # Bloqueia a solicitação durante a operação.
        # Isso evita que duas retiradas sejam registradas
        # simultaneamente para a mesma solicitação.
        solicitacao = db.exec(
            select(Solicitacao)
            .where(
                Solicitacao.solicitacao_id == solicitacao_id
            )
            .with_for_update()
        ).first()

        if solicitacao is None:
            raise ValueError("Solicitação não encontrada.")

        if solicitacao.status_solicitacao != SolicitacaoStatus.Aprovada:
            raise ValueError(
                "Somente solicitações aprovadas podem gerar empréstimos."
            )

        # Verifica se a solicitação já possui empréstimo.
        emprestimo_existente = db.exec(
            select(Emprestimo).where(
                Emprestimo.solicitacao_id == solicitacao_id
            )
        ).first()

        if emprestimo_existente is not None:
            raise ValueError(
                "Esta solicitação já possui um empréstimo registrado."
            )

        # Bloqueia o equipamento para evitar retiradas
        # simultâneas de solicitações diferentes.
        equipamento = db.exec(
            select(Equipamento)
            .where(
                Equipamento.equipamento_id == solicitacao.equipamento_id
            )
            .with_for_update()
        ).first()

        if equipamento is None:
            raise ValueError("Equipamento não encontrado.")

        if (
            equipamento.equipamento_status_equipamento
            != EquipamentoStatus.Disponivel
        ):
            raise ValueError(
                "O equipamento não está disponível para retirada."
            )

        # Cria o empréstimo.
        emprestimo = Emprestimo(
            solicitacao_id=solicitacao_id,
            responsavel_retirada_id=responsavel_id,
            status_emprestimo=EmprestimoStatus.Ativo
        )

        # Atualiza a situação do equipamento.
        equipamento.equipamento_status_equipamento = (
            EquipamentoStatus.Emprestado
        )

        db.add(emprestimo)
        db.add(equipamento)

        # Salva as duas alterações na mesma transação.
        db.commit()
        db.refresh(emprestimo)

        return emprestimo

    except ValueError:
        db.rollback()
        raise

    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(
            "Erro ao registrar a retirada no banco de dados."
        ) from e

    except Exception:
        db.rollback()
        raise


# =========================
# LISTAR TODOS OS EMPRÉSTIMOS
# =========================

def listar_emprestimos(db: Session):
    try:
        statement = (
            select(Emprestimo)
            .order_by(Emprestimo.emprestimo_id.desc())
        )

        return db.exec(statement).all()

    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(
            "Erro ao consultar os empréstimos."
        ) from e


# =========================
# LISTAR EMPRÉSTIMOS ATIVOS
# =========================

def listar_emprestimos_ativos(db: Session):
    try:
        statement = (
            select(Emprestimo)
            .where(
                Emprestimo.status_emprestimo == EmprestimoStatus.Ativo
            )
            .order_by(Emprestimo.emprestimo_id.desc())
        )

        return db.exec(statement).all()

    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(
            "Erro ao consultar os empréstimos ativos."
        ) from e


# =========================
# LISTAR EMPRÉSTIMOS DO USUÁRIO
# =========================

def listar_emprestimos_usuario(
    db: Session,
    usuario_id: int
):
    try:
        statement = (
            select(Emprestimo)
            .join(
                Solicitacao,
                Emprestimo.solicitacao_id == Solicitacao.solicitacao_id
            )
            .where(
                Solicitacao.usuario_id == usuario_id
            )
            .order_by(Emprestimo.emprestimo_id.desc())
        )

        return db.exec(statement).all()

    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(
            "Erro ao consultar os empréstimos do usuário."
        ) from e


# =========================
# BUSCAR EMPRÉSTIMO POR ID
# =========================

def buscar_emprestimo(
    db: Session,
    emprestimo_id: int
):
    try:
        emprestimo = db.get(Emprestimo, emprestimo_id)

        if emprestimo is None:
            raise ValueError("Empréstimo não encontrado.")

        return emprestimo

    except ValueError:
        raise

    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(
            "Erro ao consultar o empréstimo."
        ) from e


# =========================
# VERIFICAR PROPRIETÁRIO
# =========================

def verificar_proprietario(
    db: Session,
    emprestimo_id: int,
    usuario_id: int
):
    try:
        statement = (
            select(Emprestimo)
            .join(
                Solicitacao,
                Emprestimo.solicitacao_id == Solicitacao.solicitacao_id
            )
            .where(
                Emprestimo.emprestimo_id == emprestimo_id,
                Solicitacao.usuario_id == usuario_id
            )
        )

        emprestimo = db.exec(statement).first()

        return emprestimo is not None

    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(
            "Erro ao verificar o empréstimo do usuário."
        ) from e

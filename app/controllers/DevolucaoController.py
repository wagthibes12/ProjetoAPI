
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError

from entidades.models import (
    Devolucao,
    DevolucaoCriacao,
    Emprestimo,
    EmprestimoStatus,
    Solicitacao,
    Equipamento,
    EquipamentoStatus
)


# =========================
# REGISTRAR DEVOLUÇÃO
# =========================

def registrar_devolucao(
    db: Session,
    emprestimo_id: int,
    dados: DevolucaoCriacao,
    responsavel_id: int
):
    try:
        # Bloqueia o empréstimo durante a operação.
        emprestimo = db.exec(
            select(Emprestimo)
            .where(
                Emprestimo.emprestimo_id == emprestimo_id
            )
            .with_for_update()
        ).first()

        if emprestimo is None:
            raise ValueError("Empréstimo não encontrado.")

        if emprestimo.status_emprestimo != EmprestimoStatus.Ativo:
            raise ValueError(
                "Somente empréstimos ativos podem receber devolução."
            )

        # Verifica se já existe uma devolução.
        devolucao_existente = db.exec(
            select(Devolucao)
            .where(
                Devolucao.emprestimo_id == emprestimo_id
            )
        ).first()

        if devolucao_existente is not None:
            raise ValueError(
                "Este empréstimo já possui uma devolução registrada."
            )

        # Busca a solicitação vinculada ao empréstimo.
        solicitacao = db.get(
            Solicitacao,
            emprestimo.solicitacao_id
        )

        if solicitacao is None:
            raise ValueError(
                "Solicitação vinculada ao empréstimo não encontrada."
            )

        # Bloqueia o equipamento durante a devolução.
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
            != EquipamentoStatus.Emprestado
        ):
            raise ValueError(
                "O equipamento não está registrado como emprestado."
            )

        # Cria o registro da devolução.
        devolucao = Devolucao(
            emprestimo_id=emprestimo_id,
            responsavel_recebimento_id=responsavel_id,
            observacao=dados.observacao
        )

        # Finaliza o empréstimo.
        emprestimo.status_emprestimo = EmprestimoStatus.Finalizado

        # Atualiza a situação do equipamento.
        if dados.encaminhar_manutencao:
            equipamento.equipamento_status_equipamento = (
                EquipamentoStatus.Manutencao
            )
        else:
            equipamento.equipamento_status_equipamento = (
                EquipamentoStatus.Disponivel
            )

        # Salva todas as alterações na mesma transação.
        db.add(devolucao)
        db.add(emprestimo)
        db.add(equipamento)

        db.commit()
        db.refresh(devolucao)

        return devolucao

    except ValueError:
        db.rollback()
        raise

    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(
            "Erro ao registrar a devolução no banco de dados."
        ) from e

    except Exception:
        db.rollback()
        raise


# =========================
# LISTAR TODAS AS DEVOLUÇÕES
# =========================

def listar_devolucoes(db: Session):
    try:
        statement = (
            select(Devolucao)
            .order_by(Devolucao.devolucao_id.desc())
        )

        return db.exec(statement).all()

    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(
            "Erro ao consultar as devoluções."
        ) from e


# =========================
# BUSCAR DEVOLUÇÃO POR ID
# =========================

def buscar_devolucao(
    db: Session,
    devolucao_id: int
):
    try:
        devolucao = db.get(
            Devolucao,
            devolucao_id
        )

        if devolucao is None:
            raise ValueError("Devolução não encontrada.")

        return devolucao

    except ValueError:
        raise

    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(
            "Erro ao consultar a devolução."
        ) from e

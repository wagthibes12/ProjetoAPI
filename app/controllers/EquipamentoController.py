
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError

from entidades.models import (
    Equipamento,
    EquipamentoStatus
)


# =========================
# BUSCAR TODOS OS EQUIPAMENTOS
# =========================

def buscar_todos_equipamentos(db: Session):
    try:
        statement = (
            select(Equipamento)
            .order_by(Equipamento.equipamento_id.desc())
        )

        return db.exec(statement).all()

    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(
            "Falha ao consultar os equipamentos no banco de dados."
        ) from e


# =========================
# CADASTRAR EQUIPAMENTO
# =========================

def cadastrar_equipamento(
    equipamento_data: Equipamento,
    db: Session
):
    try:
        # Impede que o ID seja informado pelo usuário.
        dados = equipamento_data.model_dump(
            exclude={"equipamento_id"}
        )

        equipamento = Equipamento(**dados)

        db.add(equipamento)
        db.commit()
        db.refresh(equipamento)

        return equipamento

    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(
            "Não foi possível cadastrar o equipamento no banco de dados."
        ) from e


# =========================
# ATUALIZAR EQUIPAMENTO
# =========================

def atualizar_equipamento(
    db: Session,
    equipamento_id: int,
    equipamento_data: Equipamento
):
    try:
        # Bloqueia o registro durante a atualização.
        statement = (
            select(Equipamento)
            .where(
                Equipamento.equipamento_id == equipamento_id
            )
            .with_for_update()
        )

        equipamento = db.exec(statement).first()

        if equipamento is None:
            raise KeyError("Equipamento não encontrado.")

        # Não permite alterar o ID do equipamento.
        dados = equipamento_data.model_dump(
            exclude_unset=True,
            exclude={"equipamento_id"}
        )

        for campo, valor in dados.items():
            setattr(equipamento, campo, valor)

        db.add(equipamento)
        db.commit()
        db.refresh(equipamento)

        return equipamento

    except (KeyError, ValueError):
        db.rollback()
        raise

    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(
            "Não foi possível atualizar o equipamento no banco de dados."
        ) from e


# =========================
# DELETAR EQUIPAMENTO
# =========================

def deletar_equipamento(
    db: Session,
    equipamento_id: int
):
    try:
        # Bloqueia o equipamento durante a exclusão.
        statement = (
            select(Equipamento)
            .where(
                Equipamento.equipamento_id == equipamento_id
            )
            .with_for_update()
        )

        equipamento = db.exec(statement).first()

        if equipamento is None:
            raise KeyError("Equipamento não encontrado.")

        # Não permite excluir equipamento emprestado.
        if (
            equipamento.equipamento_status_equipamento
            == EquipamentoStatus.Emprestado
        ):
            raise ValueError(
                "Não é possível excluir um equipamento que está emprestado."
            )

        db.delete(equipamento)
        db.commit()

    except (KeyError, ValueError):
        db.rollback()
        raise

    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(
            "Não foi possível excluir o equipamento. "
            "Verifique se existem solicitações ou outros registros relacionados."
        ) from e

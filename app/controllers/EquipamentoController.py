
from sqlmodel import Session, select
from entidades.models import Equipamento
from sqlalchemy.exc import OperationalError, IntegrityError


def buscar_todos_equipamentos(db: Session):
    try:
        statement = select(Equipamento)
        return db.exec(statement).all()

    except OperationalError as e:
        raise RuntimeError(
            "Falha na conexão com o banco de dados."
        ) from e


def cadastrar_equipamento(equipamento_data: Equipamento, db: Session):
    try:
        dados = equipamento_data.model_dump(exclude={"equipamento_id"})

        equipamento = Equipamento(**dados)

        db.add(equipamento)
        db.commit()
        db.refresh(equipamento)

        return equipamento

    except OperationalError as e:
        db.rollback()
        raise RuntimeError(
            "Falha na conexão com o banco de dados."
        ) from e

    except IntegrityError as e:
        db.rollback()
        raise ValueError(
            "Não foi possível cadastrar o equipamento. "
            "Verifique os dados e as restrições do banco."
        ) from e


def atualizar_equipamento(
    db: Session,
    equipamento_id: int,
    equipamento_data: Equipamento
):
    try:
        equipamento = db.get(Equipamento, equipamento_id)

        if equipamento is None:
            raise KeyError("Equipamento não encontrado.")

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

    except OperationalError as e:
        db.rollback()
        raise RuntimeError(
            "Falha na conexão com o banco de dados."
        ) from e

    except IntegrityError as e:
        db.rollback()
        raise ValueError(
            "Não foi possível atualizar o equipamento. "
            "Verifique os dados informados."
        ) from e


def deletar_equipamento(db: Session, equipamento_id: int):
    try:
        equipamento = db.get(Equipamento, equipamento_id)

        if equipamento is None:
            raise KeyError("Equipamento não encontrado.")

        db.delete(equipamento)
        db.commit()

    except OperationalError as e:
        db.rollback()
        raise RuntimeError(
            "Falha na conexão com o banco de dados."
        ) from e

    except IntegrityError as e:
        db.rollback()
        raise ValueError(
            "Não foi possível excluir o equipamento. "
            "Verifique se existem registros relacionados."
        ) from e

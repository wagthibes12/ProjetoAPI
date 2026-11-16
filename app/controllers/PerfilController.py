
from sqlmodel import Session, select
from sqlalchemy.exc import OperationalError, IntegrityError

from entidades.models import Perfil


def inserir_perfil(perfil: Perfil, db: Session):
    try:
        db.add(perfil)
        db.commit()
        db.refresh(perfil)

        return perfil

    except OperationalError as e:
        db.rollback()
        raise RuntimeError(
            "Falha de conexão com o banco de dados ao tentar cadastrar o perfil."
        ) from e

    except IntegrityError as e:
        db.rollback()
        raise ValueError(
            "Este perfil já está cadastrado no sistema."
        ) from e


def buscar_todos_os_perfis(db: Session):
    try:
        statement = select(Perfil)
        return db.exec(statement).all()

    except OperationalError as e:
        db.rollback()
        raise RuntimeError(
            "Falha de conexão com o banco de dados ao tentar buscar todos os perfis."
        ) from e


def deletar_perfil(db: Session, perfil_id: int):
    try:
        perfil = db.get(Perfil, perfil_id)

        if perfil is None:
            raise KeyError("Perfil não encontrado.")

        db.delete(perfil)
        db.commit()

    except IntegrityError as e:
        db.rollback()
        raise ValueError(
            "Não é possível deletar este perfil."
        ) from e

    except OperationalError as e:
        db.rollback()
        raise RuntimeError(
            "Falha de comunicação com o banco de dados."
        ) from e


def atualizar_perfil(
    db: Session,
    perfil_id: int,
    dados_atualizados: Perfil
) -> Perfil:
    try:
        perfil = db.get(Perfil, perfil_id)

        if perfil is None:
            raise KeyError("Perfil informado não localizado.")

        perfil_data = dados_atualizados.model_dump(
            exclude_unset=True,
            exclude={"id_perfil"}
        )

        for key, value in perfil_data.items():
            setattr(perfil, key, value)

        db.add(perfil)
        db.commit()
        db.refresh(perfil)

        return perfil

    except IntegrityError as e:
        db.rollback()
        raise ValueError(
            "Erro de integridade nos dados fornecidos."
        ) from e

    except OperationalError as e:
        db.rollback()
        raise RuntimeError(
            "Falha de comunicação com o banco de dados."
        ) from e


from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError

from entidades.models import Perfil


# =========================
# INSERIR PERFIL
# =========================

def inserir_perfil(
    perfil: Perfil,
    db: Session
):
    try:
        dados = perfil.model_dump(
            exclude={"id_perfil"}
        )

        perfil_insert = Perfil(**dados)

        db.add(perfil_insert)
        db.commit()
        db.refresh(perfil_insert)

        return perfil_insert

    except SQLAlchemyError as e:
        db.rollback()

        mensagem = str(e).lower()

        if "duplicate" in mensagem or "unique" in mensagem:
            raise ValueError(
                "Este perfil já está cadastrado no sistema."
            ) from e

        raise RuntimeError(
            "Falha ao cadastrar o perfil no banco de dados."
        ) from e


# =========================
# BUSCAR TODOS OS PERFIS
# =========================

def buscar_todos_os_perfis(
    db: Session
):
    try:
        statement = (
            select(Perfil)
            .order_by(Perfil.id_perfil)
        )

        return db.exec(statement).all()

    except SQLAlchemyError as e:
        db.rollback()

        raise RuntimeError(
            "Falha ao buscar os perfis no banco de dados."
        ) from e


# =========================
# DELETAR PERFIL
# =========================

def deletar_perfil(
    db: Session,
    perfil_id: int
):
    try:
        perfil = db.get(
            Perfil,
            perfil_id
        )

        if perfil is None:
            raise KeyError("Perfil não encontrado.")

        db.delete(perfil)
        db.commit()

    except KeyError:
        db.rollback()
        raise

    except SQLAlchemyError as e:
        db.rollback()

        raise ValueError(
            "Não é possível excluir este perfil. "
            "Verifique se existem usuários vinculados a ele."
        ) from e


# =========================
# ATUALIZAR PERFIL
# =========================

def atualizar_perfil(
    db: Session,
    perfil_id: int,
    dados_atualizados: Perfil
) -> Perfil:

    try:
        perfil = db.get(
            Perfil,
            perfil_id
        )

        if perfil is None:
            raise KeyError("Perfil informado não localizado.")

        perfil_data = dados_atualizados.model_dump(
            exclude_unset=True,
            exclude={"id_perfil"}
        )

        for campo, valor in perfil_data.items():
            setattr(perfil, campo, valor)

        db.add(perfil)
        db.commit()
        db.refresh(perfil)

        return perfil

    except KeyError:
        db.rollback()
        raise

    except SQLAlchemyError as e:
        db.rollback()

        mensagem = str(e).lower()

        if "duplicate" in mensagem or "unique" in mensagem:
            raise ValueError(
                "Já existe um perfil cadastrado com esses dados."
            ) from e

        raise RuntimeError(
            "Falha ao atualizar o perfil no banco de dados."
        ) from e


from entidades.models import CategoriaEquipamento
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError


# =========================
# INSERIR CATEGORIA
# =========================

def inserir_categoria(
    categoria: CategoriaEquipamento,
    db: Session
):
    try:
        dados = categoria.model_dump(
            exclude={"categoria_id"}
        )

        categoria_insert = CategoriaEquipamento(**dados)

        db.add(categoria_insert)
        db.commit()
        db.refresh(categoria_insert)

        return categoria_insert

    except SQLAlchemyError as e:
        db.rollback()

        mensagem = str(e).lower()

        if "duplicate" in mensagem or "unique" in mensagem:
            raise ValueError(
                "Esta categoria já está cadastrada no sistema."
            ) from e

        raise RuntimeError(
            "Falha ao cadastrar a categoria no banco de dados."
        ) from e


# =========================
# BUSCAR TODAS AS CATEGORIAS
# =========================

def buscar_todas_categoria_equipamento(
    db: Session
):
    try:
        statement = (
            select(CategoriaEquipamento)
            .order_by(CategoriaEquipamento.categoria_id.desc())
        )

        return db.exec(statement).all()

    except SQLAlchemyError as e:
        db.rollback()

        raise RuntimeError(
            "Falha ao buscar categorias no banco de dados."
        ) from e


# =========================
# DELETAR CATEGORIA
# =========================

def deletar_categoria(
    db: Session,
    categoria_id: int
):
    try:
        categoria = db.get(
            CategoriaEquipamento,
            categoria_id
        )

        if categoria is None:
            raise KeyError("Categoria não encontrada.")

        db.delete(categoria)
        db.commit()

    except KeyError:
        db.rollback()
        raise

    except SQLAlchemyError as e:
        db.rollback()

        raise ValueError(
            "Não foi possível excluir esta categoria. "
            "Verifique se existem registros relacionados."
        ) from e


# =========================
# ATUALIZAR CATEGORIA
# =========================

def atualizar_categoria(
    db: Session,
    categoria_id: int,
    dados_atualizados: CategoriaEquipamento
) -> CategoriaEquipamento:

    try:
        categoria = db.get(
            CategoriaEquipamento,
            categoria_id
        )

        if categoria is None:
            raise KeyError("Categoria não encontrada.")

        categoria_data = dados_atualizados.model_dump(
            exclude_unset=True,
            exclude={"categoria_id"}
        )

        for campo, valor in categoria_data.items():
            setattr(categoria, campo, valor)

        db.add(categoria)
        db.commit()
        db.refresh(categoria)

        return categoria

    except KeyError:
        db.rollback()
        raise

    except SQLAlchemyError as e:
        db.rollback()

        mensagem = str(e).lower()

        if "duplicate" in mensagem or "unique" in mensagem:
            raise ValueError(
                "Já existe uma categoria cadastrada com essa descrição."
            ) from e

        raise RuntimeError(
            "Falha ao atualizar a categoria no banco de dados."
        ) from e

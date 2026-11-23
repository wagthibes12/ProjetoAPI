
from sqlmodel import Session, select
from sqlalchemy.exc import SQLAlchemyError

from entidades.models import (
    Usuario,
    UsuarioCriacao,
    UsuarioAtualizacao,
)

from core.security import cria_hash_senha


# =========================
# INSERIR USUÁRIO
# =========================

def inserir_usuario(
    usuario: UsuarioCriacao,
    db: Session
):
    try:
        dados = usuario.model_dump(
            exclude={"senha"}
        )

        # Converte a senha em hash antes de salvar.
        dados["senha_hash"] = cria_hash_senha(
            usuario.senha
        )

        usuario_insert = Usuario(**dados)

        db.add(usuario_insert)
        db.commit()
        db.refresh(usuario_insert)

        return usuario_insert

    except SQLAlchemyError as e:
        db.rollback()

        mensagem = str(e).lower()

        if "duplicate" in mensagem or "unique" in mensagem:
            raise ValueError(
                "Já existe um usuário cadastrado com este documento ou e-mail."
            ) from e

        raise RuntimeError(
            "Falha ao cadastrar o usuário no banco de dados."
        ) from e


# =========================
# BUSCAR TODOS OS USUÁRIOS
# =========================

def buscar_todos_os_usuarios(
    db: Session
):
    try:
        statement = (
            select(Usuario)
            .order_by(Usuario.id_usuario)
        )

        return db.exec(statement).all()

    except SQLAlchemyError as e:
        db.rollback()

        raise RuntimeError(
            "Falha ao buscar os usuários no banco de dados."
        ) from e


# =========================
# BUSCAR USUÁRIO POR ID
# =========================

def buscar_usuario_por_id(
    db: Session,
    usuario_id: int
):
    try:
        usuario = db.get(
            Usuario,
            usuario_id
        )

        if usuario is None:
            raise KeyError("Usuário não encontrado.")

        return usuario

    except KeyError:
        raise

    except SQLAlchemyError as e:
        db.rollback()

        raise RuntimeError(
            "Falha ao consultar o usuário no banco de dados."
        ) from e


# =========================
# DELETAR USUÁRIO
# =========================

def deletar_usuario(
    db: Session,
    usuario_id: int
):
    try:
        usuario = db.get(
            Usuario,
            usuario_id
        )

        if usuario is None:
            raise KeyError("Usuário não encontrado.")

        db.delete(usuario)
        db.commit()

    except KeyError:
        db.rollback()
        raise

    except SQLAlchemyError as e:
        db.rollback()

        raise ValueError(
            "Não é possível excluir este usuário, pois ele pode estar "
            "relacionado a outras informações do sistema."
        ) from e


# =========================
# ATUALIZAR USUÁRIO
# =========================

def atualizar_usuario(
    db: Session,
    usuario_id: int,
    dados_atualizados: UsuarioAtualizacao
):
    try:
        usuario = db.get(
            Usuario,
            usuario_id
        )

        if usuario is None:
            raise KeyError("Usuário informado não localizado.")

        dados = dados_atualizados.model_dump(
            exclude_unset=True,
            exclude={"id_usuario", "senha_hash"}
        )

        # Se uma nova senha foi informada, gera outro hash.
        nova_senha = dados.pop("senha", None)

        if nova_senha:
            dados["senha_hash"] = cria_hash_senha(
                nova_senha
            )

        for campo, valor in dados.items():
            setattr(usuario, campo, valor)

        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        return usuario

    except KeyError:
        db.rollback()
        raise

    except SQLAlchemyError as e:
        db.rollback()

        mensagem = str(e).lower()

        if "duplicate" in mensagem or "unique" in mensagem:
            raise ValueError(
                "Já existe outro usuário cadastrado com este documento ou e-mail."
            ) from e

        raise RuntimeError(
            "Falha ao atualizar o usuário no banco de dados."
        ) from e

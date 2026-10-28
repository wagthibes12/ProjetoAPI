
from sqlmodel import Session, select
from sqlalchemy.exc import OperationalError, IntegrityError

from entidades.models import (
    Usuario,
    UsuarioCriacao,
    UsuarioAtualizacao,
)
from core.security import cria_hash_senha


def inserir_usuario(usuarioa: UsuarioCriacao, db: Session):
    try:
        dados = usuarioa.model_dump(exclude={"senha"})
        dados["senha_hash"] = cria_hash_senha(usuarioa.senha)

        usuario_insert = Usuario(**dados)

        db.add(usuario_insert)
        db.commit()
        db.refresh(usuario_insert)

        return usuario_insert

    except OperationalError as e:
        db.rollback()
        raise RuntimeError(
            "Falha de conexão com o banco de dados ao cadastrar o usuário."
        ) from e

    except IntegrityError as e:
        db.rollback()
        raise ValueError(
            "Não foi possível cadastrar o usuário. "
            "Verifique se o documento, e-mail ou perfil já estão cadastrados."
        ) from e


def buscar_todos_os_usuarios(db: Session):
    try:
        statement = select(Usuario)
        return db.exec(statement).all()

    except OperationalError as e:
        db.rollback()
        raise RuntimeError(
            "Falha de conexão com o banco de dados ao buscar os usuários."
        ) from e


def buscar_usuario_por_id(db: Session, usuario_id: int):
    try:
        usuario = db.get(Usuario, usuario_id)

        if usuario is None:
            raise KeyError("Usuário não encontrado.")

        return usuario

    except OperationalError as e:
        db.rollback()
        raise RuntimeError(
            "Falha de comunicação com o banco de dados."
        ) from e


def deletar_usuario(db: Session, usuario_id: int):
    try:
        usuario = db.get(Usuario, usuario_id)

        if usuario is None:
            raise KeyError("Usuário não encontrado.")

        db.delete(usuario)
        db.commit()

    except IntegrityError as e:
        db.rollback()
        raise ValueError(
            "Não é possível deletar este usuário, pois ele pode estar "
            "relacionado a outras informações do sistema."
        ) from e

    except OperationalError as e:
        db.rollback()
        raise RuntimeError(
            "Falha de comunicação com o banco de dados."
        ) from e


def atualizar_usuario(
    db: Session,
    usuario_id: int,
    dados_atualizados: UsuarioAtualizacao
):
    try:
        usuario = db.get(Usuario, usuario_id)

        if usuario is None:
            raise KeyError("Usuário informado não localizado.")

        dados = dados_atualizados.model_dump(exclude_unset=True)

        # Se uma nova senha foi enviada, armazena somente o hash.
        nova_senha = dados.pop("senha", None)

        if nova_senha:
            dados["senha_hash"] = cria_hash_senha(nova_senha)

        for chave, valor in dados.items():
            setattr(usuario, chave, valor)

        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        return usuario

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

from sqlmodel import Session, select
from sqlalchemy.exc import OperationalError, IntegrityError

from entidades.models import Usuario, Perfil
from core.security import verifica_senha, criar_token


def fazer_login(db: Session, email: str, password: str):
    try:
        
        usuario = db.exec(
            select(Usuario).where(Usuario.email == email)
        ).first()

        
        senha_valida = (
            usuario is not None
            and verifica_senha(password, usuario.senha_hash)
        )

        if not senha_valida:
            raise ValueError("Credenciais inválidas")

        
        perfil = db.get(Perfil, usuario.perfil_id)

        if perfil is None:
            raise ValueError("Perfil do usuário não encontrado")

        
        token = criar_token(
            str(usuario.id_usuario),
            role=perfil.rotulo
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    except (IntegrityError, OperationalError) as e:
        db.rollback()
        raise RuntimeError(
            "Falha ao consultar o banco de dados durante o login."
        ) from e
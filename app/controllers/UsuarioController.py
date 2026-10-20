from sqlmodel import Session, select
from sqlalchemy.exc import OperationalError, IntegrityError
from entidades.models import Usuario
from pydantic import ValidationError



def inserir_usuario(usuarioa:Usuario,
                      db:Session):
    try:
        usuario_insert = Usuario.model_validate(Usuario)
        db.add(usuario_insert)
        db.commit()
        db.refresh(usuario_insert)
        return usuario_insert 
    except ValidationError as e:
        raise ValueError("Verifique os dados informados") from e
    except OperationalError as e:
        db.rollback ()
        raise RuntimeError ("Falha de conexão com o banco de dados ao tentar cadastrar o usuário.") from e
    except IntegrityError as e:
        db.rollback ()
        raise ValueError ("Não foi possivel cadastrar o usuário. Verifique se o documento," 
                          "e-mail ou perfil já estao cadastrados") from e

def buscar_todos_os_usuarios(db:Session):
   try:
        statement = select (Usuario)
        result = db.exec(statement).all()
        return result
   except OperationalError as e:
       db.rollback()
       raise RuntimeError("Falha de conexão com o banco de dados ao tentar buscar todos os usuários.") from e

def buscar_usuario_por_id(db: Session, usuario_id: int):
    try:
        usuario = db.get (Usuario, usuario_id)
        if not usuario:
            raise KeyError("Usuário não encontrado")
        return usuario
    except OperationalError as e:
        db.rollback()
        raise RuntimeError(
            "Falha de comunicação com o banco de dados."
        )  from e
     

def deletar_usuario(db: Session, usuario_id: int):
    try:
        usuario = db.get(Usuario, usuario_id)
        if not usuario:
            raise KeyError (f"Usuário não encontrado.")
        db.delete(usuario)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise ValueError ("Não é possivel deletar este usuário, pois ele pode estar" 
                          "relacionado a outras informações do sistema") from e
    except OperationalError as e:
        db.rollback()
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e

def atualizar_usuario(db: Session, usuario_id: int, dados_atualizados: Usuario) -> Usuario:
    try:
        usuario = db.get (Usuario, usuario_id)
        if not usuario:
            raise KeyError(f"Usuário informado não localizado.")
        usuario_data = dados_atualizados.model_dump(exclude_unset=True)
        for key, value in usuario_data.items():
            setattr(usuario, key, value) 

        db.add(usuario)
        db.commit()
        db.refresh(usuario)

        return usuario
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Erro de integridade nos dados fornecidos.") from e

    except OperationalError as e:
        db.rollback()
        raise RuntimeError ("Falha de comunicação com o banco de dados.") from e 
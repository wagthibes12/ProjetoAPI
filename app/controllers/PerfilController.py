from entidades.models import Perfil
from sqlmodel import Session,select
from sqlalchemy.exc import OperationalError,IntegrityError
from pydantic import ValidationError

def inserir_perfil(perfil:Perfil,
                      db:Session):
    try:
        perfil_insert = Perfil.model_validate(perfil)
        db.add(perfil_insert)
        db.commit()
        db.refresh(perfil_insert)
        return perfil_insert
    except ValidationError as e:
        raise ValueError("Verifique os dados informados") from e
    except OperationalError as e:
        db.rollback ()
        raise RuntimeError ("Falha de conexão com o banco de dados ao tentar cadastrar o perfil.") from e
    except IntegrityError as e:
        db.rollback ()
        raise ValueError ("Este Perfil ja está cadastrado no sistema") from e

def buscar_todos_os_perfis(db:Session):
   try:
        statement = select (Perfil)
        result = db.exec(statement).all()
        return result
   except OperationalError as e:
       db.rollback()
       raise RuntimeError("Falha de conexão com o banco de dados ao tentar buscar todos os perfis.") from e

def deletar_perfil(db: Session, perfil_id: int):
    try:
        perfil  = db.get(Perfil, perfil_id)
        if not perfil:
            raise KeyError (f" Perfil não encontrado.")
        db.delete(perfil)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise ValueError ("Não é possivel deletar este Perfil") from e
    except OperationalError as e:
        db.rollback()
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e

def atualizar_perfil(db: Session, perfil_id: int, dados_atualizados: Perfil) -> Perfil:
    try:
        perfil = db.get (Perfil, perfil_id)
        if not perfil:
            raise KeyError(f"Perfil informado não localizado.")
        perfil_data = dados_atualizados.model_dump(exclude_unset=True)
        for key, value in perfil_data.items():
            setattr(perfil, key, value) 

        db.add(perfil)
        db.commit()
        db.refresh(perfil)

        return perfil
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Erro de integridade nos dados fornecidos.") from e

    except OperationalError as e:
        db.rollback()
        raise RuntimeError ("Falha de comunicação com o banco de dados.") from e 

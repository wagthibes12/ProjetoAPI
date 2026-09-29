####     codigo se estiver Chave Estrangeira FK   #######


from sqlmodel import Session
from entidades.models import Equipamento,CategoriaEquipamento
from sqlalchemy.exc import OperationalError, IntegrityError

def cadastrar_equipamento(equipamento_data: Equipamento,db : Session):
    try:

        equipamento = Equipamento(**equipamento_data.model_dump())
        db.add(equipamento)
        db.commit()
        db.refresh(equipamento)

    except OperationalError as e:
        raise RuntimeError("Falha na conexão com o banco de dados") from e
    except IntegrityError as e:
        raise ValueError ("Verifique os dados Informados") from e
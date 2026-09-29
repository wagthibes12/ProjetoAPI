from entidades.models import CategoriaEquipamento
from sqlmodel import Session,select
from sqlalchemy.exc import OperationalError,IntegrityError
from pydantic import ValidationError

def inserir_categoria(categoria:CategoriaEquipamento,
                      db:Session):
    try:
        categoria_insert = CategoriaEquipamento.model_validate(categoria)
        db.add(categoria_insert)
        db.commit()
        db.refresh(categoria_insert)
        return categoria_insert
    except ValidationError as e:
        raise ValueError("Verifique os dados informados") from e
    except OperationalError as e:
        db.rollback ()
        raise RuntimeError ("Falha de conexão com o banco de dados ao tentar cadastrar a categoria.") from e
    except IntegrityError as e:
        db.rollback ()
        raise ValueError ("Esta categoria ja está cadastrada no sistema") from e

def buscar_todas_categoria_equipamento(db:Session):
   try:
        statement = select (CategoriaEquipamento)
        result = db.exec(statement).all()
        return result
   except OperationalError as e:
       db.rollback()
       raise RuntimeError("Falha de conexão com o banco de dados ao tentar buscar categorias.") from e

def deletar_categoria(db: Session, categoria_id: int):
    try:
        categoria = db.get(CategoriaEquipamento, categoria_id)
        if not categoria:
            raise KeyError (f" Categoria não encontrada.")
        db.delete(categoria)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise ValueError ("Não é possivel deletar esta categoria pois existem equipamentos vinculadas a ela.") from e
    except OperationalError as e:
        db.rollback()
        raise RuntimeError("Falha de comunicação com o banco de dados.") from e

def atualizar_categoria(db: Session, categoria_id: int, dados_atualizados: CategoriaEquipamento) -> CategoriaEquipamento:
    try:
        categoria = db.get (CategoriaEquipamento, categoria_id)
        if not categoria:
            raise KeyError(f"Categoria informada não localizada.")
        categoria_data = dados_atualizados.model_dump(exclude_unset=True)
        for key, value in categoria_data.items():
            setattr(categoria, key, value) 

        db.add(categoria)
        db.commit()
        db.refresh(categoria)

        return categoria
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Erro de integridade nos dados fornecidos.") from e

    except OperationalError as e:
        db.rollback()
        raise RuntimeError ("Falha de comunicação com o banco de dados.") from e       
    
        
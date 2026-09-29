from sqlmodel import SQLModel, Field
from enum import Enum
from typing import Optional

class PerfilBase(SQLModel):
    nome: str = Field(min_length=2,max_length=50)
    rotulo: str = Field(min_length=2,max_length=50)
    descricao: str = Field(max_length=255)


class Perfil(PerfilBase, table=True):
    __tablename__ = "perfis"
    id_perfil: int | None = Field(default=None,primary_key=True)

class CategoriaEquipamento(SQLModel,table= True):
    __tablename__= "categoria_equipamentos"
    categoria_id : int | None = Field(default=None,primary_key=True)
    categoria_descricao : str = Field(max_length=100)
    #equipamentos : list["Equipamento"] 
    
    
#############################################################################

class EquipamentoStatus (str,Enum):
    Disponivel= "Disponivel"
    Emprestado= "Emprestado"
    Manutencao= "Manutencao"
    Baixado= "Baixado"

class EquipamentoBase(SQLModel):
    equipamento_nome: str  = Field(min_length=3,max_length=100)
    equipamento_patrimonio : str  = Field(min_length=3,max_length=10)
    equipamento_descricao : str = Field(max_length=255)
    equipamento_status_equipamento: EquipamentoStatus = Field(default=EquipamentoStatus.Disponivel)

class Equipamento(EquipamentoBase,table=True):
     __tablename__="equipamento"
     equipamento_id: int | None =  Field(default=None,primary_key=True)
#     categoria: CategoriaEquipamento = Relationship(back_populates="Equipamento")

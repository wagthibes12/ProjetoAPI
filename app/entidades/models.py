
from sqlmodel import SQLModel, Field
from enum import Enum
from datetime import datetime, date
from pydantic import BaseModel, ConfigDict


class UsuarioLogin(BaseModel):
    email: str
    senha: str


class UsuarioLogado(BaseModel):
    id: int
    nome: str
    email: str
    role: str


# =========================
# PERFIS
# =========================

class PerfilBase(SQLModel):
    nome: str = Field(min_length=2, max_length=50)
    rotulo: str = Field(min_length=2, max_length=50)
    descricao: str = Field(max_length=255)


class Perfil(PerfilBase, table=True):
    __tablename__ = "perfis"

    id_perfil: int | None = Field(
        default=None,
        primary_key=True
    )


# =========================
# CATEGORIAS
# =========================

class CategoriaEquipamento(SQLModel, table=True):
    __tablename__ = "categoria_equipamentos"

    categoria_id: int | None = Field(
        default=None,
        primary_key=True
    )

    categoria_descricao: str = Field(max_length=100)


# =========================
# USUÁRIOS
# =========================

class UsuarioBase(SQLModel):
    nome_completo: str = Field(
        min_length=3,
        max_length=100
    )

    documento: str = Field(
        min_length=5,
        max_length=20
    )

    email: str = Field(max_length=100)

    curso: str | None = None

    perfil_id: int = Field(
        foreign_key="perfis.id_perfil"
    )


class Usuario(UsuarioBase, table=True):
    __tablename__ = "usuarios"

    id_usuario: int | None = Field(
        default=None,
        primary_key=True
    )

    senha_hash: str


class UsuarioCriacao(UsuarioBase):
    senha: str = Field(
        min_length=8,
        max_length=128
    )


class UsuarioAtualizacao(BaseModel):
    nome_completo: str | None = Field(
        default=None,
        min_length=3,
        max_length=100
    )

    documento: str | None = Field(
        default=None,
        min_length=5,
        max_length=20
    )

    email: str | None = Field(
        default=None,
        max_length=100
    )

    curso: str | None = None

    senha: str | None = Field(
        default=None,
        min_length=8,
        max_length=128
    )

    perfil_id: int | None = None


class UsuarioResposta(UsuarioBase):
    model_config = ConfigDict(from_attributes=True)

    id_usuario: int


# =========================
# EQUIPAMENTOS
# =========================

class EquipamentoStatus(str, Enum):
    Disponivel = "Disponivel"
    Emprestado = "Emprestado"
    Manutencao = "Manutencao"
    Baixado = "Baixado"


class EquipamentoBase(SQLModel):
    equipamento_nome: str = Field(
        min_length=3,
        max_length=100
    )

    equipamento_patrimonio: str = Field(
        min_length=3,
        max_length=10
    )

    equipamento_descricao: str = Field(
        max_length=255
    )

    equipamento_status_equipamento: EquipamentoStatus = Field(
        default=EquipamentoStatus.Disponivel
    )


class Equipamento(EquipamentoBase, table=True):
    __tablename__ = "equipamento"

    equipamento_id: int | None = Field(
        default=None,
        primary_key=True
    )


# =========================
# SOLICITAÇÕES
# =========================

class SolicitacaoStatus(str, Enum):
    Pendente = "Pendente"
    Aprovada = "Aprovada"
    Rejeitada = "Rejeitada"
    Cancelada = "Cancelada"


class SolicitacaoBase(SQLModel):
    usuario_id: int = Field(
        foreign_key="usuarios.id_usuario"
    )

    equipamento_id: int = Field(
        foreign_key="equipamento.equipamento_id"
    )

    data_prevista_retirada: date

    data_prevista_devolucao: date

    status_solicitacao: SolicitacaoStatus = Field(
        default=SolicitacaoStatus.Pendente
    )

    observacao: str | None = Field(
        default=None,
        max_length=255
    )

    responsavel_id: int | None = Field(
        default=None,
        foreign_key="usuarios.id_usuario"
    )

    data_analise: datetime | None = None


class Solicitacao(SolicitacaoBase, table=True):
    __tablename__ = "solicitacoes"

    solicitacao_id: int | None = Field(
        default=None,
        primary_key=True
    )

    data_solicitacao: datetime = Field(
        default_factory=datetime.now
    )


class SolicitacaoCriacao(SQLModel):
    equipamento_id: int
    data_prevista_retirada: date
    data_prevista_devolucao: date
    observacao: str | None = Field(
        default=None,
        max_length=255
    )


class SolicitacaoResposta(SolicitacaoBase):
    model_config = ConfigDict(from_attributes=True)

    solicitacao_id: int
    data_solicitacao: datetime


from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


# =========================
# CAMINHO DO PROJETO
# =========================

# Caminho da pasta raiz do ProjetoAPI.
PASTA_PROJETO = Path(__file__).resolve().parents[2]


# =========================
# CONFIGURAÇÕES
# =========================

class Settings(BaseSettings):

    # SSH
    ssh_host: str
    ssh_port: int = 22
    ssh_user: str
    ssh_key_path: str | None = None
    ssh_password: str | None = None

    # MariaDB
    db_host: str = "127.0.0.1"
    db_port: int = 3306
    db_name: str
    db_user: str
    db_password: str

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_EXPIRE_MINUTES: int = 15
    JWT_REFRESH_EXPIRE_DAY: int = 7
    JWT_REFRESH_EXPIRE_DAYS: int = 7
    JWT_ISSUER: str = "sistema-emprestimo"

    # =========================
    # VALIDAÇÕES
    # =========================

    @field_validator("JWT_SECRET_KEY")
    @classmethod
    def validar_chave_jwt(cls, valor: str):
        if not valor or not valor.strip():
            raise ValueError(
                "A chave secreta JWT não pode estar vazia."
            )

        return valor

    @field_validator("JWT_ACCESS_EXPIRE_MINUTES")
    @classmethod
    def validar_expiracao_access(cls, valor: int):
        if valor <= 0:
            raise ValueError(
                "O tempo de expiração do Access Token deve ser positivo."
            )

        return valor

    @field_validator(
        "JWT_REFRESH_EXPIRE_DAY",
        "JWT_REFRESH_EXPIRE_DAYS"
    )
    @classmethod
    def validar_expiracao_refresh(cls, valor: int):
        if valor <= 0:
            raise ValueError(
                "O tempo de expiração do Refresh Token deve ser positivo."
            )

        return valor

    # =========================
    # CONFIGURAÇÃO DO PYDANTIC
    # =========================

    model_config = SettingsConfigDict(
        env_file=PASTA_PROJETO / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# =========================
# INSTÂNCIA DAS CONFIGURAÇÕES
# =========================

settings = Settings()

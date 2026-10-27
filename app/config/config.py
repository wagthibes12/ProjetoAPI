
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Caminho da pasta raiz do projeto ProjetoAPI
PASTA_PROJETO = Path(__file__).resolve().parents[2]


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

    model_config = SettingsConfigDict(
        env_file=PASTA_PROJETO / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# Variável que armazena os valores lidos do arquivo .env
settings = Settings()



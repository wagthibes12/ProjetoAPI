
from dataclasses import dataclass, field
from typing import Generator
import urllib.parse

from sshtunnel import SSHTunnelForwarder
from sqlalchemy.engine import Engine
from sqlmodel import create_engine, Session

from config.config import settings


@dataclass
class Database:

    _tunel: SSHTunnelForwarder | None = field(
        default=None,
        init=False
    )

    _engine: Engine | None = field(
        default=None,
        init=False
    )

    # =========================
    # INICIALIZAÇÃO
    # =========================

    def __post_init__(self):
        self.start_tunnel()

    # =========================
    # INICIAR TÚNEL SSH
    # =========================

    def start_tunnel(self):

        try:
            # Abre o túnel SSH.
            self._tunel = SSHTunnelForwarder(
                (settings.ssh_host, settings.ssh_port),

                ssh_username=settings.ssh_user,

                ssh_password=settings.ssh_password,

                ssh_pkey=settings.ssh_key_path,

                remote_bind_address=(
                    settings.db_host,
                    settings.db_port
                )
            )

            self._tunel.start()

            # Codifica a senha para utilização na URL.
            encoded_password = urllib.parse.quote_plus(
                settings.db_password
            )

            # Monta a URL de conexão com o MySQL/MariaDB.
            url = (
                f"mysql+pymysql://{settings.db_user}:{encoded_password}"
                f"@127.0.0.1:{self._tunel.local_bind_port}"
                f"/{settings.db_name}"
            )

            # Cria o mecanismo de conexão.
            self._engine = create_engine(
                url,
                echo=False,
                pool_pre_ping=True
            )

        except Exception:
            # Encerra o engine caso tenha sido criado.
            if self._engine is not None:
                self._engine.dispose()
                self._engine = None

            # Encerra o túnel caso tenha sido iniciado.
            if self._tunel is not None:
                self._tunel.stop()
                self._tunel = None

            raise

    # =========================
    # DISPONIBILIZAR SESSÃO
    # =========================

    def get_db(self) -> Generator[Session, None, None]:

        if self._engine is None:
            raise ConnectionError(
                "O mecanismo de conexão com o banco não foi inicializado."
            )

        with Session(self._engine) as session:
            yield session

    # =========================
    # ENCERRAR CONEXÃO
    # =========================

    def close(self):

        # Encerra o engine.
        if self._engine is not None:
            self._engine.dispose()
            self._engine = None

        # Encerra o túnel SSH.
        if self._tunel is not None:
            self._tunel.stop()
            self._tunel = None


# =========================
# INSTÂNCIA DO BANCO
# =========================

database = Database()

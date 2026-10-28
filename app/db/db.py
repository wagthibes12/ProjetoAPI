
from dataclasses import dataclass, field
from sshtunnel import SSHTunnelForwarder
from sqlalchemy.engine import Engine
from config.config import settings
import urllib.parse

from sqlmodel import create_engine, Session


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

    def __post_init__(self):
        self.start_tunnel()

    def start_tunnel(self):
        try:
            self._tunel = SSHTunnelForwarder(
                (settings.ssh_host, settings.ssh_port),
                ssh_username=settings.ssh_user,
                ssh_password=settings.ssh_password,
                remote_bind_address=(
                    settings.db_host,
                    settings.db_port
                )
            )

            self._tunel.start()

            encoded_password = urllib.parse.quote_plus(
                settings.db_password
            )

            url = (
                f"mysql+pymysql://{settings.db_user}:{encoded_password}"
                f"@127.0.0.1:{self._tunel.local_bind_port}"
                f"/{settings.db_name}"
            )

            self._engine = create_engine(
                url,
                echo=True
            )

        except Exception:
            if self._tunel is not None:
                self._tunel.stop()
                self._tunel = None

            raise

    def get_db(self):
        if self._engine is None:
            raise ConnectionError(
                "O mecanismo de conexão com o banco não foi inicializado."
            )

        with Session(self._engine) as session:
            yield session

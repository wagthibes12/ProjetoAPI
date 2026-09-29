from dataclasses import dataclass
from sshtunnel import SSHTunnelForwarder    
from config.config import settings
import urllib  
from sqlmodel import create_engine, Session 


@dataclass
class Database():
    _tunel : SSHTunnelForwarder | None = None
    _engine : None = None
    def __post_init__(self):
        self._tunel = self.start_tunnel()

    def start_tunnel(self):
        self._tunel = SSHTunnelForwarder(
            (settings.ssh_host,settings.ssh_port),
            ssh_username=settings.ssh_user,
            ssh_password=settings.ssh_password,
            remote_bind_address=(settings.db_host,settings.db_port)
        ) 
        self._tunel.start()
        encoded_passworld = urllib.parse.quote_plus(settings.db_password)
        url = ( f"mysql+pymysql://{settings.db_user}:{encoded_passworld}"
                f"@127.0.0.1:{self._tunel.local_bind_port}/{settings.db_name}"    
                )
        self._engine = create_engine(
            url,
            echo=True
        )
        if not self._engine:
            raise ConnectionError("Erro de conexão com o banco de dados")

    def get_db(self):
        with Session(self._engine) as s:
            yield s  
        
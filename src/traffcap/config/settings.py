from typing import Optional
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    requests_prefix: str = "r"
    frontend_path: Optional[Path] = None
    server_url: str = ""
    websocket_protocol: str = "ws"
    http_protocol: str = "http"
    db_user: str = ""
    db_password: str = ""
    db_host: str = ""
    db_name: str = ""
    db_driver: str = ""

    class Config:
        env_prefix: str = "traffcap_"
        env_file: str = ".env"

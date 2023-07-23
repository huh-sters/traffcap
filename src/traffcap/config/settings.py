from typing import Optional
from pathlib import Path
from pydantic import BaseSettings


class Settings(BaseSettings):
    requests_prefix: str = "r"
    frontend_path: Optional[Path] = None
    server_url: str = ""
    websocket_protocol: str = "ws"
    http_protocol: str = "http"

    class Config:
        env_prefix: str = "traffcap_"
        env_file: str = ".env"

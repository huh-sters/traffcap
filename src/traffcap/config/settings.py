from typing import Optional
from pathlib import Path
from pydantic import BaseSettings


class Settings(BaseSettings):
    requests_prefix: str = "r"
    frontend_path: Optional[Path] = None

    class Config:
        env_prefix: str = "traffcap_"
        env_file: str = ".env"

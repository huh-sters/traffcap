from pydantic import BaseSettings


class Settings(BaseSettings):
    requests_prefix: str = "r"
    frontend_path: str = None

    class Config:
        env_prefix: str = "traffcap_"
        env_file: str = ".env"

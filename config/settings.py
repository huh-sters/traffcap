from pydantic import BaseSettings


class Settings(BaseSettings):
    requests_prefix: str = "r"

    class Config:
        env_prefix: str = "traffcap_"
        env_file: str = ".env"
